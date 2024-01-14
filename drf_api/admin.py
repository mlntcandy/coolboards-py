from django.contrib import admin
from import_export import resources
from coolboards.models import Item, ItemCategory, ItemPhoto, Manufacturer

# Register your models here.


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item

    def dehydrate_category(self, item):
        return item.category.name

    def dehydrate_manufacturer(self, item):
        return item.manufacturer.name

    def dehydrate_price(self, item):
        return f"{item.price} руб."

    def dehydrate_discount(self, item):
        return f"{item.discount} руб."

    def dehydrate_new(self, item):
        return "Да" if item.new else "Нет"

    def dehydrate_stock(self, item):
        return f"{item.stock} шт."

    def get_export_headers(self):
        headers = super().get_export_headers()
        header_names = {
            "name": "Название",
            "description": "Описание",
            "price": "Цена",
            "discount": "Скидка",
            "new": "Новинка",
            "stock": "Количество на складе",
            "category": "Категория",
            "manufacturer": "Производитель",
        }
        headers = [header_names.get(header, header) for header in headers]
        return headers


class ItemCategoryResource(resources.ModelResource):
    class Meta:
        model = ItemCategory


class ItemPhotoResource(resources.ModelResource):
    class Meta:
        model = ItemPhoto


class ManufacturerResource(resources.ModelResource):
    class Meta:
        model = Manufacturer
