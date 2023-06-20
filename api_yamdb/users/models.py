from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        validators=([RegexValidator(
            regex=r'^(?!me$).*$',
            message='Неподходящий логин. "me" использовать запрещено.')]))
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

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
