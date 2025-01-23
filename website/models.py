import hashlib
import secrets
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField()


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Token(models.Model):
    token = models.CharField(max_length=40)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # This means the token will be deleted when the user is deleted
        related_name="tokens",  # This is optional but useful for reverse querying
    )

    def is_valid(self) -> bool:
        return self.expires_at >= timezone.now()

    @staticmethod
    def generate_random_sha1_token(length=16):
        return hashlib.sha1(secrets.token_bytes(length)).hexdigest()
