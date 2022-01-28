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
        for i in users_id:
            if instance.user.id != i:
                send_email_notice(i, instance.user, instance.text)
