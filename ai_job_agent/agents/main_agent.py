from db.db_client import get_session
from db.models import Job, UserProfile, CustomAnswer
from browser.ats_detector import detect_ats
from utils.logger import logger
from llm.llm_client import generate_text
from browser.playwright_client import BrowserClient
from llm.prompts import resume_prompt, cover_letter_prompt
import os
from utils.resume_parser import extract_resume_text
from agents.hitl import get_user_input


def resolve_field(field_name, session, job):
    field_name = field_name.lower()

    logger.info(f"[AI] Resolving field: {field_name}")

    user = session.query(UserProfile).first()

    profile_map = {
        "name": user.name,
        "custname": user.name,
        "firstname": user.name.split()[0],
        "fname": user.name.split()[0],
        "lastname": user.name.split()[-1],
        "lname": user.name.split()[-1],
        "email": user.email,
        "custemail": user.email,
        "phone": user.phone,
        "custtel": user.phone,
    }

    # ---- 1. PROFILE ----
    if field_name in profile_map:
        logger.info("[AI] Found in profile DB")
        return profile_map[field_name]

    # ---- 2. CUSTOM ANSWERS ----
    answer = session.query(CustomAnswer).filter_by(key=field_name).first()
    if answer:
        logger.info("[AI] Found in custom answers")
        return answer.value

    # ---- 3. SKIP IRRELEVANT ----
    skip_keywords = ["search", "filter", "toggle", "dark", "quiz"]

    if any(k in field_name for k in skip_keywords):
        logger.info("[AI] Skipping irrelevant field")
        return None

    # ---- 4. AI INFERENCE ----
    logger.info("[AI] Using AI inference")

    prompt = f"""
You are an AI job assistant.

Field: {field_name}

Candidate:
- AI/ML Engineer
- 3 years experience

Generate a realistic professional answer.
"""

    ai_answer = generate_text(prompt)

    # ---- 5. HITL ----
    if ai_answer == "N/A" or not ai_answer:
        logger.info(f"[HITL] Need user input for: {field_name}")

        user_ans = get_user_input(
            f"Enter value for '{field_name}' (30s timeout): "
        )

        if user_ans:
            session.add(CustomAnswer(key=field_name, value=user_ans))
            session.commit()
            logger.info("[HITL] Saved for future use")
            return user_ans

        else:
            logger.warning("[HITL] Timeout → moving to backlog")

            # 🔥 REQUIRED: backlog + unanswered tracking
            if not job.unanswered_fields:
                job.unanswered_fields = []

            job.unanswered_fields.append(field_name)
            job.status = "backlog"

            return None

    return ai_answer


def run_agent():
    session = get_session()
    jobs = session.query(Job).filter_by(status="pending").all()

    for job in jobs:
        logger.info(f"Processing job: {job.title}")

        browser = BrowserClient()

        try:
            # ---- ATS DETECTION ----
            job.ats = detect_ats(job.url)
            logger.info(f"[ATS] Detected: {job.ats}")

            # ---- DOC GENERATION ----
            generate_documents(job)

            browser.open(job.url)

            form_fields = browser.get_form_fields()

            if not form_fields:
                logger.warning("[INFO] No form detected — likely external ATS flow")

                job.status = "partial"

                continue

            # ---- REMOVE DUPLICATES ----
            seen = set()
            unique_fields = []

            for field in form_fields:
                name = field["name"]
                if name not in seen:
                    seen.add(name)
                    unique_fields.append(field)

            form_fields = unique_fields

            logger.info(f"Detected fields: {form_fields}")

            # ---- FIELD LOOP ----
            for field in form_fields:
                field_name = field["name"]

                logger.info(f"Processing field: {field_name}")

                answer = resolve_field(field_name, session, job)

                if job.status == "backlog":
                    logger.warning("Stopping job → moved to backlog")
                    break

                if answer:
                    browser.fill_field(field, answer)

            # ---- SUBMIT ONLY IF NOT BACKLOG ----
            if job.status != "backlog":
                browser.submit()
                job.status = "applied"

        except Exception as e:
            job.status = "failed"
            job.failure_reason = str(e)

        finally:
            browser.close()

        session.commit()

    session.close()


def generate_documents(job):
    os.makedirs("outputs", exist_ok=True)

    session = get_session()
    user = session.query(UserProfile).first()

    resume_text = extract_resume_text(user.resume_path)

    resume_content = generate_text(
        resume_prompt(job.title, job.company, resume_text)
    )

    cover_letter_content = generate_text(
        cover_letter_prompt(job.title, job.company)
    )

    with open(f"outputs/resume_{job.id}.txt", "w", encoding="utf-8") as f:
        f.write(resume_content)

    with open(f"outputs/cover_letter_{job.id}.txt", "w", encoding="utf-8") as f:
        f.write(cover_letter_content)

    logger.info(f"Generated resume for job {job.id}")
    logger.info(f"Generated cover letter for job {job.id}")

    session.close()