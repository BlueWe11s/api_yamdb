from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class Users(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = ((USER, 'user'), (MODERATOR, 'moderator'), (ADMIN, 'admin'))
    username = models.CharField(
        'Логин',
        max_length=50,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator())
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.is_staff or self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    def __str__(self):
        return self.username
