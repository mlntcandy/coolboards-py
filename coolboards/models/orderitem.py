from django.db import models
from .item import Item
from django.apps import apps


class OrderItem(models.Model):
    order = models.ForeignKey(
        "coolboards.Order", on_delete=models.CASCADE, verbose_name="Заказ"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
