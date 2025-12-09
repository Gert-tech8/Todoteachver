import os
import smtplib
import ssl
from email.message import EmailMessage

def send_otp_email(to_email: str, otp_code: int | str) -> None:
    """
    Send OTP to the user's email using SMTP settings from environment variables.
    If SMTP settings are not provided, this will print the OTP to stdout (dev fallback).
    """
    otp_code = str(otp_code)  # ensure string
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)

    subject = "Your OTP for Todo Application"
    body = f"Your verification OTP is: {otp_code}\n\nIf you didn't request this, ignore this message."

    if not smtp_host or not smtp_user or not smtp_password:
        # Development fallback
        print(f"[DEV EMAIL] OTP for {to_email}: {otp_code}")
        return

    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print(f"OTP email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send OTP email to {to_email}: {e}")
