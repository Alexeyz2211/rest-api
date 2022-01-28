from celery import shared_task
from django.core.mail import send_mail

from authentication.models import User
from support.settings import EMAIL_HOST_USER


@shared_task
def send_email_notice(i, sender, text):
    user = User.objects.get(id=i)
    send_mail(str(sender),
              text,
              EMAIL_HOST_USER,
              user)
    return None

