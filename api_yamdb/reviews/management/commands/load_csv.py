import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import (Category, Comments, Genre, GenreTitle, Review,
                            Title)
from users.models import User

MODELS_AND_FILES = {

    Category: 'category.csv',
    User: 'users.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comments: 'comments.csv',
    }


FOREIGN_KEY_FIELDS = ('category', 'author')


class Command(BaseCommand):
    """Команда для чтения csv файлов и добавления информации в базу."""

    help = 'импорт данных из .csv'

    def handle(self, *args, **kwargs):
        for model, datafile_csv in MODELS_AND_FILES.items():
            with open(f'{settings.BASE_DIR}/static/data/{datafile_csv}',
                      'r',
                      encoding='utf-8',) as csv_file:
                csv_data = csv.DictReader(csv_file)
                objects = []
                for row in csv_data:
                    for field in FOREIGN_KEY_FIELDS:
                        if field in row:
                            row[f'{field}_id'] = row[field]
                            del row[field]
                    objects.append(model(**row))
                try:
                    model.objects.bulk_create(objects)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Загрузка {datafile_csv}  завершена'))
                except Exception as error:
                    self.stderr.write('Упс, загрухка {datafile_csv}'
                                      f'не удалась: {error}')


# python manage.py load_csv

# https://code.tutsplus.com/ru/tutorials/how-to-read-and-write-csv-files-in-python--cms-29907
# https://stacktuts.com/how-to-import-csv-data-into-django-models
