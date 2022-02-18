from typing import Any, Dict

from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from .tasks import send_email_notice


@receiver(post_save, sender=models.Message)
def on_post_save(instance: models.Message, created: bool, **kwargs: Dict[str, Any]):
    if created:
        users = models.Message.objects.filter(ticket__message=instance.id)
        users_id = set([u.user.id for u in users])
        for user_id in users_id:
            if instance.user.id != user_id:
                send_email_notice.delay(user_id, instance.user.username, instance.text)
