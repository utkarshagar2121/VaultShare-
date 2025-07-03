# utils.py
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def send_verification_email(email_to: str, verify_url: str):
    print("inside this verification")
    email = EmailMessage()
    email['From'] = os.getenv("EMAIL_FROM")
    email['To'] = email_to
    email['Subject'] = 'Verify Your Email'

    email.set_content(f"Click the link to verify your email:\n{verify_url}")

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            smtp.send_message(email)
            print(f"✅ Email sent to {email_to}")
    except Exception as e:
        print("❌ Failed to send email:", e)



import cloudinary
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


