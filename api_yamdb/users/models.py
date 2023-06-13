from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        validators=([RegexValidator(regex=r'^[\w.@+-]+$')]))
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',)
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя',
                                  blank=True)
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия',
                                 blank=True)
    bio = models.TextField(verbose_name='О себе',
                           blank=True)
    role = models.CharField(max_length=150,
                            verbose_name='Роль',
                            choices=USER_ROLES,
                            default=USER)

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
