from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime


User = get_user_model()


class Category(models.Model):
    """Категории."""
    name = models.CharField('наименование категории', max_length=256)
    slug = models.SlugField('slug', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""
    name = models.CharField('имя жанра', max_length=256)
    slug = models.SlugField('slug', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Произведения."""

    name = models.CharField('Наименоввание', max_length=256)
    year = models.IntegerField(
        'год создания',
        validators=[MaxValueValidator(
            int(datetime.now().year),
            message='Год не должен быть больше текущего')])
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True,
        verbose_name='Категория')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genre, related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


# class GenreTitle(models.Model):
#     """Для загрузки csv."""
#     title = models.ForeignKey(Titles, on_delete=models.CASCADE)
#     genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Соответствие жанра и произведения'
#         verbose_name_plural = 'Таблица соответствия жанров и произведений'

#     def __str__(self):
#         return f'{self.title} принадлежит жанру/ам {self.genre}'


class Reviews(models.Model):
    """Отзыв к произведению."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Titles,
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
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date', )

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Комментарий к отзыву."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text

