from django.core.validators import MaxValueValidator
from django.db import models
from datetime import datetime


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
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True,
        verbose_name='Категория')
    genre = models.ManyToManyField(Genre, related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
