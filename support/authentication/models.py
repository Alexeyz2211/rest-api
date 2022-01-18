from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.EmailField(max_length=64, unique=True, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.username
