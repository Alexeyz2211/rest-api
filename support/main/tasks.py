from celery import shared_task
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from authentication.models import User
from support.settings import EMAIL_HOST_USER


@shared_task
def send_email_notice(user_id, sender_email, text):
    user = (get_object_or_404(User, pk=user_id).username, )
    send_mail(
        sender_email,
        text,
        EMAIL_HOST_USER,
        user
    )
