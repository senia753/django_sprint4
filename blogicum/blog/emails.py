from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(user_email):
    subject = 'Добро пожаловать на наш сайт!'
    html_message = render_to_string('emails/welcome.html',
                                    {'email': user_email})
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        'noreply@yourdomain.com',
        [user_email],
        html_message=html_message,
        fail_silently=False,
    )
