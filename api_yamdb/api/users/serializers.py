from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers

from users.validators import validate_username

User = get_user_model()


class AuthSerializer(serializers.Serializer):
    """
    Сериализатор для обработки запроса на получени кода подтверждения
    """
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True, max_length=150,
        validators=(validate_username, UnicodeUsernameValidator())
    )

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Одно из полей username или email уже занято'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор для обработки
    """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio'
        )
