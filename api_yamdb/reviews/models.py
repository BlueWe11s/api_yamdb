from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import Users
from reviews.constants import NAME_LENGTH, SLUG_LENGTH

User = Users


class Category(models.Model):
    '''
    Категории
    '''
    name = models.CharField('Наименование', max_length=NAME_LENGTH)
    slug = models.SlugField(
        'Уникальный идентификатор',
        max_length=SLUG_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''
    Жанры
    '''
    name = models.CharField('Наименование', max_length=NAME_LENGTH)
    slug = models.SlugField(
        'Уникальный идентификатор',
        max_length=SLUG_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name


class Title(models.Model):
    '''
    Произведения
    '''
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    name = models.CharField('Наименование', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.TextField("Описание произведения")

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'title'

    def __str__(self):
        return self.name


class Review(models.Model):
    '''
    Отзывы
    '''
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='Автор отзыва'
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        default_related_name = 'reviews'
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return (self.text)[:15]


class Comment(models.Model):
    '''
    Комментарии
    '''
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Комментарий')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        default_related_name = 'comments'
        ordering = ['pub_date']
        verbose_name = 'Комментрий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (self.text)
