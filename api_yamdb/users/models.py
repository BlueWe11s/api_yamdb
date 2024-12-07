from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username

class Users(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = ((USER, 'user'), (MODERATOR, 'moderator'), (ADMIN, 'admin'))
    username = models.CharField(
        'Логин', max_length=50, unique=True, validators=[validate_username]
    )
    role = models.CharField(
        'Роль', max_length=50, choices=ROLE_CHOICES, default=USER
    )
    email = models.EmailField(
        'Почта', max_length=320, unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=50, blank=True
    )
    bio = models.TextField(
        'Биография',
        max_length=2000,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (self.role == self.ADMIN
                or self.is_superuser
                or self.is_staff)

    def __str__(self):
        return self.username
