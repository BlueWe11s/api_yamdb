import re
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            "Вы не можете выбрать никнейм 'me', "
            "выберите другой никнейм.")
