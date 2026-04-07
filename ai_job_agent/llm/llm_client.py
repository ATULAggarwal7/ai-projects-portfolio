from utils.logger import logger


def generate_text(prompt):
    logger.warning("Using intelligent fallback generator")

    if "resume" in prompt.lower():
        return generate_resume(prompt)

    if "cover letter" in prompt.lower():
        return generate_cover_letter(prompt)

    return "N/A"


# -------- RESUME --------
def generate_resume(prompt):
    # extract some info from prompt
    role = "AI/ML Engineer"
    company = "the company"

    if "target role:" in prompt.lower():
        role = prompt.split("Target Role:")[-1].split("\n")[0].strip()

    if "company:" in prompt.lower():
        company = prompt.split("Company:")[-1].split("\n")[0].strip()

    return f"""
ATUL AGGARWAL
{role}

SUMMARY:
AI/ML Engineer with 3+ years experience applying for {role} at {company}.
Strong background in building intelligent systems, automation pipelines, and scalable AI solutions.

SKILLS:
Python, Machine Learning, Deep Learning, APIs, Automation

EXPERIENCE:
- Built AI systems aligned with {role} requirements
- Developed automation tools for real-world use cases
- Worked on AI-driven pipelines

PROJECTS:
- AI Job Application Agent (Current Project)
  → Automated job applications using AI agents, browser automation, and LLM-based reasoning
- Predictive Maintenance System
  → Built IoT + ML system for failure prediction

EDUCATION:
Bachelor’s Degree in Computer Science

"""


# -------- COVER LETTER --------
def generate_cover_letter(prompt):
    if "company:" in prompt.lower():
        company = prompt.split("Company:")[-1].strip().split("\n")[0]
    else:
        company = "your company"

    if "role:" in prompt.lower():
        role = prompt.split("Role:")[-1].strip().split("\n")[0]
    else:
        role = "AI/ML Engineer"

    return f"""
Dear Hiring Manager,

I am excited to apply for the {role} position at {company}. 

With 3+ years of experience in AI/ML, I have built intelligent systems and automation pipelines aligned with business needs.

I believe my skills match well with this role and I would love to contribute to your team.

Best regards,  
Atul Aggarwal
"""