from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def generate_confirmation_code(user):
    """
    Функция для генерации кода подтверждения
    """
    confirmation_code = default_token_generator.make_token(user)
    return confirmation_code


def send_conformaton_mail(user):
    """
    Функция для отправки кода подтврждения
    """
    confirmation_code = generate_confirmation_code(user)
    subject = 'Ваш код подтверждения API_YaMDB'
    message = f'{confirmation_code}'
    recipient_list = [user.email]

    send_mail(subject, message, DEFAULT_FROM_EMAIL, recipient_list,
              fail_silently=True)
