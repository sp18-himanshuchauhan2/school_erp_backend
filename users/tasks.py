from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email_task(email, name, password, role, school_name):
    subject = f"Welcome to {school_name} - Registered as {role.title()}"
    message = f"""
Hi {name},

You have been successfully registered as a {role} at {school_name} in the School ERP system.

Your login credentials are:
Email: {email}
Password: {password}

Please keep this information safe. You can log in using your role's portal.

Regards,
{school_name} - School ERP Team
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
