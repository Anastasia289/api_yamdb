from django.contrib import admin
from reviews import models


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year',
                    'description', 'category')
    search_fields = ('name',)

    empty_value_display = '-пусто-'


admin.site.register(models.Title, TitlesAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Category)
admin.site.register(models.Review)
admin.site.register(models.Comments)
admin.site.register(models.GenreTitle)
