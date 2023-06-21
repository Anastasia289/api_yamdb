import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews import models
from users.models import User

MODELS_AND_FILES = {
    models.Category: 'category.csv',
    User: 'users.csv',
    models.Genre: 'genre.csv',
    models.Title: 'titles.csv',
    models.GenreTitle: 'genre_title.csv',
    models.Review: 'review.csv',
    models.Comments: 'comments.csv',
}


FOREIGN_KEYS = ('category', 'author')


class Command(BaseCommand):
    """Команда для чтения csv файлов и добавления информации в базу."""

    help = 'импорт данных из .csv'

    def handle(self, *args, **kwargs):
        for model, datafile_csv in MODELS_AND_FILES.items():
            with open(f'{settings.BASE_DIR}/static/data/{datafile_csv}',
                      'r',
                      encoding='utf-8',) as csv_file:
                csv_data = csv.DictReader(csv_file)
                prepared_for_creating_objects = []
                for row in csv_data:
                    for field in FOREIGN_KEYS:
                        if field in row:
                            row[f'{field}_id'] = row[field]
                            del row[field]
                    prepared_for_creating_objects.append(model(**row))
                try:
                    model.objects.bulk_create(prepared_for_creating_objects)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Загрузка {datafile_csv}  завершена'))
                except Exception as error:
                    self.stderr.write('Упс, загрухка {datafile_csv}'
                                      f'не удалась: {error}')
                    print(settings.DEBUG)
