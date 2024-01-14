from django.contrib import admin
from django.db import models


class ItemPhoto(models.Model):
    photo = models.ImageField(upload_to="item_photos/", verbose_name="Фото")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    main = models.BooleanField(default=False, verbose_name="Основное")

    name = models.CharField(max_length=255, null=True, verbose_name="Название")

    def __str__(self):
        return str(self.added_at) + " - " + (self.name or self.photo.name)

    def get_item(self):
        return self.item_set.first()

    get_item.short_description = "Товар"

    class Meta:
        verbose_name = "Фотография товара"
        verbose_name_plural = "Фотографии товаров"
