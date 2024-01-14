from django.contrib import admin
from django.db import models
from simple_history.models import HistoricalRecords
from simple_history.admin import SimpleHistoryAdmin


class Manufacturer(models.Model):
    history = HistoricalRecords()

    photo = models.ImageField(
        upload_to="manufacturers/", null=True, verbose_name="Фото"
    )

    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(verbose_name="Слаг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


@admin.register(Manufacturer)
class ManufacturerAdmin(SimpleHistoryAdmin):
    list_display = ["name", "slug"]
    list_display_links = ["name", "slug"]
    search_fields = ["name", "slug"]
