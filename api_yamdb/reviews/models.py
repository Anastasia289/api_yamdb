from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

MAX_NAME_LENGTH = 256
MAX_SLUG_LENGTH = 50


class PubDate(models.Model):
    """Абстрактная модель для времени"""

    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
        )

    class Meta:
        abstract = True

    def __str__(self):
        return self.pub_date


class Category(models.Model):
    """Категории."""
    name = models.CharField('наименование категории',
                            max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('slug', unique=True, max_length=MAX_SLUG_LENGTH)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""
    name = models.CharField('имя жанра', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('slug', unique=True, max_length=MAX_SLUG_LENGTH)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField('Наименование', max_length=MAX_NAME_LENGTH)
    year = models.IntegerField(
        'год создания',
        validators=[MaxValueValidator(
            int(datetime.now().year),
            message='Год не должен быть больше текущего')])
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True,
        verbose_name='Категория',)
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle', related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(PubDate):
    """Отзыв к произведению."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )
    # pub_date = models.DateTimeField(
    #     'Дата добавления',
    #     auto_now_add=True,
    #     db_index=True
    # )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date', )
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_for_title'
            ),
        )

    def __str__(self):
        return self.text


class Comments(PubDate):
    """Комментарий к отзыву."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    # pub_date = models.DateTimeField(
    #     'Дата добавления',
    #     auto_now_add=True,
    #     db_index=True
    # )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    """Модель для загрузки данных. Сопоставляет жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Жанры-произведение'
        verbose_name_plural = 'Жанры-произведения'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} - {self.genre}'
