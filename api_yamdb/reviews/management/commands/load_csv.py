import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (Category,
                            Comments,
                            Genre,
                            GenreTitle,
                            Reviews,
                            Titles)
from users.models import User


TABLES = {

    Category: 'category.csv',
    User: 'users.csv',
    Genre: 'genre.csv',
    Titles: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Reviews: 'review.csv',
    Comments: 'comments.csv',
    }


FOREIGN_KEY_FIELDS = ('category', 'author')


class Command(BaseCommand):
    help = 'импорт данных из .csv'

    def handle(self, *args, **kwargs):
        for model, datafile_csv in TABLES.items():
            with open(f'{settings.BASE_DIR}/static/data/{datafile_csv}',
                      'r',
                      encoding='utf-8',) as csv_file:
                csv_data = csv.DictReader(csv_file)  # https://code.tutsplus.com/ru/tutorials/how-to-read-and-write-csv-files-in-python--cms-29907
                objects = []
                for row in csv_data:
                    for field in FOREIGN_KEY_FIELDS:
                        if field in row:
                            row[f'{field}_id'] = row[field]
                            del row[field]
                    objects.append(model(**row))
                    print(objects)
                model.objects.bulk_create(objects)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Загрузка {datafile_csv}  завершена'))

# python manage.py load_csv

# https://stacktuts.com/how-to-import-csv-data-into-django-models
