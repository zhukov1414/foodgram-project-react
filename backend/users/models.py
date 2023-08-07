from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Уникальный юзернейм',
        unique=True,
        validators=[validate_username,],
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты. Обязательное поле.',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='subscriber'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscription'
    )
    added_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscription_unique'
            )
        ]
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
