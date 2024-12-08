from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''
    Админка категорий
    '''
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    list_filter = ('slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    '''
    Админка жанров
    '''
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    list_filter = ('slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    '''
    Админка произведений
    '''
    list_display = ('name', 'year', 'description', 'category')
    list_display_links = ('name',)
    search_fields = ('name', 'year', 'description', 'category')
    list_filter = ('name', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    '''
    Админка отзывов
    '''
    list_display = ('id', 'title', 'author', 'text', 'pub_date')
    search_fields = ('author', 'text')
    list_filter = ('author', 'title', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''
    Админка комментариев
    '''
    list_display = ('id', 'author', 'review', 'text', 'pub_date')
    search_fields = ('author', 'review')
    list_filter = ('author', 'review', 'pub_date')
