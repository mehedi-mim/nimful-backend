import smtplib
from email.message import EmailMessage
from typing import Any

from config import get_config
from utils.email import email_type_enums
from utils.email.signup_verification_mail import verification_mail


async def send_email(email, email_type: Any, **kwargs):
    try:

        if email_type == email_type_enums.MailSendType.VERIFICATION.value:
            subject = "Confirm your email address"
            body = verification_mail(kwargs, email=email)
        else:
            return
            # Email Send

        email_message = EmailMessage()
        email_message['subject'] = subject
        email_message['From'] = get_config().email_user
        email_message['To'] = email
        email_message.add_alternative(body, subtype='html')
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(get_config().email_user, get_config().email_user_password)
            smtp.send_message(email_message)
        print("Successfully sent email!")
    except Exception as e:
        print(e)
