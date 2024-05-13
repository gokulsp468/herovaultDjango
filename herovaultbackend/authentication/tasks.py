from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from celery import shared_task

@shared_task
def send_otp_email(user_email,user_otp):
    subject = 'Welcome to Our Service'
    html_message = render_to_string('email_template.html', { 'user_otp': user_otp})
    plain_message = strip_tags(html_message)  # Strip HTML tags for plain text version
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
    email.attach_alternative(html_message, "text/html")
    
    print("Email sent")
    email.send()
