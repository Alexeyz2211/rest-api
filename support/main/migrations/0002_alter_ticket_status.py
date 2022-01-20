# Generated by Django 4.0 on 2022-01-20 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[(1, 'Unsolved'), (2, 'Solved'), (3, 'Freezed')], default=(1, 'Unsolved'), max_length=12, verbose_name='Ticket_status'),
        ),
    ]