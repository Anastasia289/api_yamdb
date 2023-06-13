from django.contrib import admin

from reviews import models


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')  # здесь пока нет жанров.
    search_fields = ('name',)
    list_filter = ('year',)
    # empty_value_display = '-пусто-'


admin.site.register(models.Titles, TitlesAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Category)
