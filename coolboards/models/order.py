from django.contrib import admin
from django.db import models
from .item import Item
from .orderitem import OrderItem

from simple_history.models import HistoricalRecords
from simple_history.admin import SimpleHistoryAdmin


class PaymentMethodChoices(models.TextChoices):
    ON_PICKUP = "P", "pickup"
    ONLINE = "O", "online"


class OrderStatusChoices(models.TextChoices):
    CREATED = "N", "created"
    AWAITING_PAYMENT = "A", "awaiting_payment"
    COLLECTING = "C", "collecting"
    DELIVERING = "D", "delivering"
    DONE = "F", "done"
    CANCELLED = "X", "cancelled"


class DeliveryMethodChoices(models.TextChoices):
    PICKUP = "P"
    COURIER = "C"
    PARCEL = "S"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["item"]


class Order(models.Model):
    history = HistoricalRecords()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    first_name = models.CharField(max_length=128, verbose_name="Имя")
    last_name = models.CharField(max_length=128, verbose_name="Фамилия")
    phone = models.CharField(max_length=16, verbose_name="Телефон")
    email = models.CharField(max_length=128, verbose_name="Email")
    notes = models.TextField(verbose_name="Примечания", null=True, blank=True)

    payment_complete = models.BooleanField(verbose_name="Оплачен")
    payment_amount = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Сумма"
    )
    payment_method = models.CharField(
        max_length=1, choices=PaymentMethodChoices.choices, verbose_name="Способ оплаты"
    )

    order_status = models.CharField(
        max_length=1, choices=OrderStatusChoices.choices, verbose_name="Статус заказа"
    )
    delivery_method = models.CharField(
        max_length=1,
        choices=DeliveryMethodChoices.choices,
        verbose_name="Способ доставки",
    )

    delivery_address = models.TextField(verbose_name="Адрес доставки")
    items = models.ManyToManyField(
        Item, through=OrderItem, blank=True, verbose_name="Товары"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
