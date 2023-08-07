import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(username):
    if username in settings.RESERVED_USERNAMES:
        raise ValidationError(f'Имя пользователя {username} зарезервировано.')
    wrong_symbols = re.findall(settings.VALID_USERNAME, username)
    if wrong_symbols:
        wrong_symbols = str(set(''.join(wrong_symbols)))
        raise ValidationError(
            f'Символы {wrong_symbols} недопустимы в имени пользователя!',
        )
