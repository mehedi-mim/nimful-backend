import smtplib
from email.message import EmailMessage
from typing import Any

from config import get_config
from utils.email import email_type_enums
from utils.templates.reset_password_template import reset_password_mail
from utils.templates.signup_template import verification_mail
from utils.templates.invitation_template import invitation_verification_mail


async def send_email(email, email_type: Any, **kwargs):
    if email_type == email_type_enums.MailSendType.VERIFICATION.value:
        subject = "Confirm your email address"
        body = verification_mail(kwargs, email=email)
    elif email_type == email_type_enums.MailSendType.PASSWORD_RESET.value:
        subject = "Forgot password?"
        body = reset_password_mail(kwargs)
    elif email_type == email_type_enums.MailSendType.INVITATION_USER.value:
        subject = f"Join my {kwargs.get('organization_name', '')} Team on Stickler"
        body = invitation_verification_mail(kwargs)
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
