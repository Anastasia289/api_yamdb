from django.contrib import admin
from reviews import models


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year',
                    'description', 'category')  # здесь пока нет жанров.
    search_fields = ('name',)

    empty_value_display = '-пусто-'


admin.site.register(models.Titles, TitlesAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Category)
admin.site.register(models.Reviews)
admin.site.register(models.Comments)
admin.site.register(models.GenreTitle)
