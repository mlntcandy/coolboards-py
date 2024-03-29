from django.db import models
from django.contrib import admin

from .item import Item


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    user_name = models.TextField(verbose_name="Имя")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст")

    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Товар")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
