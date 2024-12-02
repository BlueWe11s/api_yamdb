from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Users(models.Model):
    role = models.CharField('Заголовок', max_length=20)
    username = models.SlugField('Уникальный идентификатор', unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user'
    )


class Title(models.Model):
    name = models.CharField('Заголовок', max_length=100)
    slug = models.SlugField('Уникальный идентификатор', unique=True)
    text = models.TextField("Описание произведения")
    score = models.IntegerField()


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор оценки",
        related_name="review"
    )
    text = models.TextField("Текст оценки")
    score = models.IntegerField()
    product = models.ForeignKey(Title, on_delete=models.CASCADE)


class Category(models.Model):
    ...


class Comments(models.Model):
    ...


class Genre(models.Model):
    ...