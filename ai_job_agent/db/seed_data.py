from db.db_client import get_session
from db.models import UserProfile, CustomAnswer, Job


def seed():
    session = get_session()

    # ---- USER ----
    user_exists = session.query(UserProfile).first()
    if not user_exists:
        user = UserProfile(
            name="Atul Aggarwal",
            email="atul@example.com",
            phone="9999999999",
            resume_path="data/resume.pdf"
        )
        session.add(user)

    # ---- CUSTOM ANSWERS ----
    answers = {
        "notice_period": "30 days",
        "expected_salary": "12 LPA",
        "relocate": "Yes",
        "visa_sponsorship": "No"
    }

    for key, value in answers.items():
        existing = session.query(CustomAnswer).filter_by(key=key).first()
        if existing:
            existing.value = value
        else:
            session.add(CustomAnswer(key=key, value=value))

    # ---- REAL JOB LINKS ----
    jobs = [
        # 🔹 SIMPLE FORMS (for clean demo — WILL WORK PERFECTLY)
        ("https://httpbin.org/forms/post", "Demo Company", "Test Role 1"),
        ("https://www.w3schools.com/html/html_forms.asp", "Demo Company", "Test Role 2"),

        # 🔹 ANOTHER SIMPLE FORM
        ("https://formspree.io/f/xayzvzvw", "Demo Company", "Test Role 3"),

        # 🔹 REAL ATS (ONLY FOR DETECTION SHOWCASE)
        ("https://boards.greenhouse.io/airbnb/jobs/5682179", "Airbnb", "Software Engineer"),
        ("https://jobs.lever.co/coinbase/6f9f5f44-6f69-4b92-8d3e-9a3c63bfa8e5", "Coinbase", "Backend Engineer"),
    ]

    for url, company, title in jobs:
        existing = session.query(Job).filter_by(url=url).first()

        if existing:
            existing.status = "pending"
            existing.failure_reason = None
            existing.unanswered_fields = None
        else:
            session.add(Job(
                url=url,
                company=company,
                title=title,
                status="pending"
            ))

    session.commit()
    session.close()


if __name__ == "__main__":
    seed()