from dotenv import load_dotenv
load_dotenv()

import os
print("SMTP_USER =", os.getenv("SMTP_USER"))
print("SMTP_PASSWORD =", os.getenv("SMTP_PASSWORD"))
print("SMTP_HOST =", os.getenv("SMTP_HOST"))

from send_mail import send_otp_email

send_otp_email("gertrudeonyema6@gmail.com", "123456")


