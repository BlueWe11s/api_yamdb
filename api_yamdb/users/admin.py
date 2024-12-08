from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Users


@admin.register(Users)
class UsersAdmin(UserAdmin):
    '''
    Админка пользователей
    '''
    list_display = ('username', 'email', 'role', 'bio',)
    search_fields = ('username', 'role', 'email',)
    list_display_links = ('username',)
    list_filter = (
        'role',
        'username',
        'is_staff',
        'if_superuser',
        'is_active',
        )
