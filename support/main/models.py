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

    class StatusInTicket(models.TextChoices):
        UNSOLVED = 'UN', 'Unsolved'
        SOLVED = 'SL', 'Solved'
        FREEZED = 'FR', 'Freezed'

    name = models.CharField('Ticket_name', max_length=128, null=True)
    description = models.TextField('Ticket_description', null=True)
    date_create = models.DateTimeField(auto_now_add=True,)
    status = models.CharField(
        'Ticket_status',
        max_length=2,
        choices=StatusInTicket.choices,
        default=StatusInTicket.UNSOLVED
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tickets',
        on_delete=models.CASCADE,
        null=True
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tickets',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'User: {self.user} created Ticket: {self.name}'
