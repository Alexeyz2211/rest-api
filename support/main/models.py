from django.conf import settings
from django.db import models


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField('Text message', null=True)
    date = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user} - {self.text}'


class Ticket(models.Model):
    name = models.CharField('Ticket_name', max_length=128, null=True)
    description = models.TextField('Ticket_description', null=True)
    date_create = models.DateTimeField(auto_now_add=True,)
    TICKET_STATUS = [
        (1, 'Unsolved'),
        (2, 'Solved'),
        (3, 'Freezed'),
    ]
    status = models.CharField('Ticket_status', max_length=12, choices=TICKET_STATUS, default=TICKET_STATUS[0])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='User',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'User: {self.user} created Ticket: {self.name}'
