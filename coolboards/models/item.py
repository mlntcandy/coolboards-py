from django.db import models
from django.contrib import admin

from .itemcategory import ItemCategory
from .manufacturer import Manufacturer
from .itemphoto import ItemPhoto

from coolboards.lib.build import compatible_categories

from simple_history.models import HistoricalRecords
from simple_history.admin import SimpleHistoryAdmin


class Item(models.Model):
    history = HistoricalRecords()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    name = models.TextField(verbose_name="Название")
    description = models.TextField(null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    # Discount is the discounted price, e.g X dollars off
    discount = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, verbose_name="Скидка"
    )
    new = models.BooleanField(verbose_name="Новинка")
    stock = models.PositiveIntegerField(verbose_name="Количество на складе")

    category = models.ForeignKey(
        ItemCategory, on_delete=models.PROTECT, verbose_name="Категория"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.PROTECT, verbose_name="Производитель"
    )

    # a photo can have only one item, but an item can have many photos
    photos = models.ManyToManyField(ItemPhoto, blank=True, verbose_name="Фотографии")

    def __str__(self):
        return self.name

    def get_main_photo(self):
        return self.photos.filter(main=True).first()

    def get_build_compatibility(self):
        # check if category is in compatible categories
        return self.category.slug in compatible_categories

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


@admin.register(Item)
class ItemAdmin(SimpleHistoryAdmin):
    list_display = [
        "id",
        "name",
        "manufacturer",
        "category",
        "price",
        "discount",
        "stock",
    ]
    list_filter = ["created_at", "new", "category"]
    date_hierarchy = "created_at"
    filter_horizontal = ["photos"]
    search_fields = ["name", "description"]
    raw_id_fields = ["manufacturer"]
    list_display_links = ["id", "name"]
