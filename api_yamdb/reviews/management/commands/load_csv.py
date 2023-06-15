# import csv

# from django.conf import settings
# from django.core.management import BaseCommand

# from reviews.models import Category, Comments, Genre, Reviews, Titles, GenreTitle
# from users.models import User


# TABLES = {

#     User: 'users.csv',  # +
#     Category: 'category.csv',  #+
#     Genre: 'genre.csv',  #+
#     Titles: 'titles.csv',  # ???????????
#     Reviews: 'review.csv',
#     Comments: 'comments.csv',
#     GenreTitle: 'genre_title.csv'
#     }

# FOREIGN_KEY_FIELDS = ('category', 'author')


# # def import_data():
# #     for model, datafile_csv in TABLES.items():
# #         with open(f'{settings.BASE_DIR}/static/data/{datafile_csv}',
# #                   'r',
# #                   encoding='utf-8',) as csv_file:
# #             reader = csv.DictReader(csv_file)
# #             objs = []
# #             for row in reader:   #&
# #                 for field in FOREIGN_KEY_FIELDS:
# #                     if field in row:
# #                         row[f'{field}_id'] = row[field]
# #                         del row[field]
# #                 objs.append(model(**row))
# #             model.objects.bulk_create(objs)

            
# # class Command(BaseCommand):
# #     help = 'Imports data from a CSV file into the YourModel model'

# #     def handle(self, *args, **options):
# #         import_data()
# #         self.stdout.write(self.style.SUCCESS('Data imported successfully'))

# # python manage.py load_csv

# # https://stacktuts.com/how-to-import-csv-data-into-django-models
# # C:\Users\bogda\OneDrive\Рабочий стол\yp\10\api_yamdb\api_yamdb\static\data\category.csv



# def csv_import(csv_data, model):
#     """Импорт данных из CSV-файла в базу данных."""

#     objects = []
#     for row in csv_data:
#         for field in FOREIGN_KEY_FIELDS:
#             if field in row:
#                 row[f'{field}_id'] = row[field]
#                 del row[field]
#         objects.append(model(**row))
#     model.objects.bulk_create(objects)


# class Command(BaseCommand):
#     help = 'импорт из .csv'

#     def handle(self, *args, **kwargs):
#         for model, datafile_csv in TABLES.items():
#             with open(f'{settings.BASE_DIR}/static/data/{datafile_csv}',
#                       'r',
#                       encoding='utf-8',) as csv_file:
#                 # reader = csv.DictReader(csv_file)
#                 csv_import(csv.DictReader(csv_file), model)
#             self.stdout.write(
#                 self.style.SUCCESS(
#                     'Загрузка завершена'
#                     )
#                 )


# class GenreTitle(models.Model):
#     """Для загрузки csv."""
#     title = models.ForeignKey(Titles, on_delete=models.CASCADE)
#     genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Соответствие жанра и произведения'
#         verbose_name_plural = 'Таблица соответствия жанров и произведений'

#     def __str__(self):
#         return f'{self.title} принадлежит жанру/ам {self.genre}'