import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


def send_email(to_email: str, subject: str, body: str) -> str:
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("APP_PASSWORD")

    if not sender_email or not sender_password:
        return "Email credentials not configured properly."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Error sending email: {str(e)}"