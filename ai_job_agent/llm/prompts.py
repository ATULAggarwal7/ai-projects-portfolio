def resume_prompt(job_title, company, resume_text):
    return f"""
You are an expert resume writer.

Candidate Resume:
{resume_text}

Target Role: {job_title}
Company: {company}

Task:
- Tailor the resume for this job
- Keep it concise and ATS-friendly
- Highlight relevant skills and experience

Return a professional resume.
"""


def cover_letter_prompt(job_title, company):
    return f"""
Write a professional cover letter for:

Role: {job_title}
Company: {company}

Candidate:
- AI/ML Engineer
- 3+ years experience

Make it:
- personalized
- confident
- concise

Return plain text.
"""