from django.contrib import admin
from django.db import models
from .item import Item
from .orderitem import OrderItem


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "first_name",
        "last_name",
        "phone",
        "email",
        "notes",
        "payment_complete",
        "payment_amount",
        "payment_method",
        "order_status",
        "delivery_method",
        "delivery_address",
        "getItems",
    ]

    def getItems(self, obj):
        items = []
        for order_item in obj.orderitem_set.all():
            item_name = order_item.item.name
            item_quantity = order_item.quantity
            items.append(f"{item_quantity}x {item_name}")
        return ";\n".join(items)

    list_filter = ("created_at", "order_status", "payment_complete")
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "items"]
    search_fields = ["first_name", "last_name", "phone", "email", "notes", "id"]
