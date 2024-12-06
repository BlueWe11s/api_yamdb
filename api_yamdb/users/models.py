from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    USER = 'user'
    MODERATOR = 'mpderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (USER, MODERATOR, ADMIN)
    username = models.CharField(
        'Логин', max_length=50, unique=True,
    )
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, default=USER
    )
    email = models.EmailField(
        'Почта', max_length=320, unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.is_superuser or self.is_staff

    def __str__(self):
        return self.username
