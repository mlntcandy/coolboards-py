from django.contrib import admin
from django.db import models


class ItemCategory(models.Model):
    photo = models.ImageField(upload_to="categories/", null=True, verbose_name="Фото")

    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(verbose_name="Слаг")

    def __str__(self):
        return self.name

    # get item count
    @admin.display(description="Количество товаров")
    def get_item_count(self):
        return self.item_set.count()

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "get_item_count"]
    list_display_links = ["name", "slug"]
    search_fields = ["name", "slug"]