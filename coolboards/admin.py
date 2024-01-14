from .models import (
    Item,
    ItemCategory,
    ItemPhoto,
    Manufacturer,
    Order,
    OrderItemInline,
    Review,
)
from django.urls import reverse
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.utils.html import format_html

from drf_api.admin import (
    ItemResource,
    ItemCategoryResource,
    ItemPhotoResource,
    ManufacturerResource,
)


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ItemResource
    list_display = [
        "id",
        "name",
        "manufacturer_link",
        "category_link",
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
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "name",
                    "description",
                    "price",
                    "discount",
                    "new",
                    "stock",
                    "category",
                    "manufacturer",
                )
            },
        ),
        ("Фотографии", {"fields": ("photos",)}),
    )

    def manufacturer_link(self, obj):
        url = reverse(
            "admin:coolboards_manufacturer_change", args=[obj.manufacturer.id]
        )
        return format_html('<a href="{}">{}</a>', url, obj.manufacturer)

    manufacturer_link.short_description = "Производитель"

    def category_link(self, obj):
        url = reverse("admin:coolboards_itemcategory_change", args=[obj.category.id])
        return format_html('<a href="{}">{}</a>', url, obj.category)

    category_link.short_description = "Категория"
    # def get_export_queryset(self, request):
    #     # add manufacturer name and category name to export
    #     return (
    #         super()
    #         .get_export_queryset(request)
    #         .select_related("manufacturer", "category")
    #         .prefetch_related("photos")
    #     )


@admin.register(ItemCategory)
class ItemCategoryAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ItemCategoryResource
    list_display = ["name", "slug", "get_item_count"]
    list_display_links = ["name", "slug"]
    search_fields = ["name", "slug"]


@admin.register(ItemPhoto)
class ItemPhotoAdmin(ImportExportModelAdmin):
    resource_class = ItemPhotoResource

    list_display = ["name", "get_item", "added_at", "main"]
    list_filter = ["added_at", "main"]
    date_hierarchy = "added_at"

    def photo(self, obj):
        # return HTML for image
        return format_html(
            '<img src="{}" alt="{}" style="max-width: 200px; max-height: 200px" />'.format(
                obj.photo.url, obj.name
            )
        )


@admin.register(Manufacturer)
class ManufacturerAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ManufacturerResource
    list_display = ["name", "slug"]
    list_display_links = ["name", "slug"]
    search_fields = ["name", "slug"]


@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "user_name",
        "rating",
        "text",
        "link_to_item",
    ]

    fields = ["user_name", "rating", "text", "item"]

    list_filter = ["created_at", "rating"]
    date_hierarchy = "created_at"
    search_fields = ["user_name", "text"]

    def link_to_item(self, obj):
        url = reverse("admin:coolboards_item_change", args=[obj.item.id])
        return format_html('<a href="{}">{}</a>', url, obj.item)

    link_to_item.short_description = "Товар"
