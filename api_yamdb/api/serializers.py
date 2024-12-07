from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_conformaton_mail
from users.validators import validate_username


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    """
    Сериализатор для обработки запроса на получение кода подтверждения.
    """
    email = serializers.EmailField(max_length=320)
    username = serializers.CharField(
        max_length=50,
        validators=[validate_username])

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()

        errors = {}
        if user_by_email != user_by_username:
            if user_by_email:
                errors['email'] = [
                    'Этот емейл используется с другим юзернейм.']
            if user_by_username:
                errors['username'] = [
                    f'Юзернейм {username} занят другим пользователем.']
            raise ValidationError(errors)

        data['user'] = user_by_email
        return data

    def create(self, validated_data):
        user = (validated_data.get('user')
                or User.objects.create(
                    email=validated_data.get('email'),
                    username=validated_data.get('username')))
        send_conformaton_mail(user)
        return user


class UsersSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class AuthUsersSerializer(UsersSerializer):
    """
    Сериализатор для модели пользователя, предназначенный для запросов,
    полученных от обычного пользователя.
    """
    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role',)


class ObtainTokenSerializer(serializers.Serializer):
    """Сериализатор для генерации токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        is_confirmation_code_correct = default_token_generator.check_token(
            user, data['confirmation_code'])
        if not is_confirmation_code_correct:
            raise serializers.ValidationError(
                'Недействительный или истекший код подтверждения.')
        data['user'] = user
        return data

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
        }
