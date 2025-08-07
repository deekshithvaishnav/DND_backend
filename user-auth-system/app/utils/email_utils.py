import os
from email.message import EmailMessage
from dotenv import load_dotenv
import aiosmtplib

load_dotenv()  # Load .env variables

async def send_reset_email(email_to: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = email_to

    reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
    msg.set_content(f"Click the link to reset your password: {reset_link}")

    await aiosmtplib.send(
        msg,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True
    )
