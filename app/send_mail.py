import os
import smtplib
import ssl
from email.message import EmailMessage



def send_otp_email(to_email: str, otp_code: str) -> None:
    """
    Send OTP to the user's email using SMTP settings from environment variables.
    If SMTP settings are not provided, this will print the OTP to stdout (dev fallback).
    Required env vars for real SMTP:
      SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM
    """
    smtp_host = "smtp.gmail.com"  # Default to Gmail SMTP
    smtp_port = 465          # Default to Gmail SMTP port
    smtp_user = "example@gmail.com"
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM")

    subject = "Your OTP for Todo Application"
    body = f"Your verification OTP is: {otp_code}\n\nIf you didn't request this, ignore this message."

    if not smtp_host or not smtp_user or not smtp_password:
        # Development fallback — print to console so you can copy the OTP during testing
        print(f"[DEV EMAIL] To: {to_email} Subject: {subject}\n{body}")
        return

    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
# ...existing code...