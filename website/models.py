import hashlib
import secrets
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.hashers import check_password


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


class PasswordHistory(models.Model):
    password = models.CharField(max_length=128)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # This means the token will be deleted when the user is deleted
        related_name="password_history",  # This is optional but useful for reverse querying
    )
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def is_in_history(user, new_password):
        passwords = (
            PasswordHistory.objects.filter(user=user)
            .order_by("-created_at")[
                : settings.PASSWORD_REQUIERMENTS.history_of_passwords
            ]
            .values_list("password", flat=True)
        )
        for password in passwords:
            if check_password(new_password, password):
                return True
        return False
