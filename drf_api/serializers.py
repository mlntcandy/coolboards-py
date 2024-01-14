from rest_framework import serializers
from coolboards.models import Review, Item, Manufacturer


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

    main_photo = serializers.SerializerMethodField()

    def get_main_photo(self, obj):
        return obj.get_main_photo().photo.url

    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        return [photo.photo.url for photo in obj.photos.all()]

    manufacturer = serializers.SerializerMethodField()

    def get_manufacturer(self, obj):
        return {
            "id": obj.manufacturer.id,
            "name": obj.manufacturer.name,
            "slug": obj.manufacturer.slug,
        }


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        if validated_data["rating"] < 1 or validated_data["rating"] > 5:
            raise serializers.ValidationError({"rating": "Rating must be in range 1-5"})
        return Review.objects.create(**validated_data)

    item = serializers.SerializerMethodField()

    def get_item(self, obj):
        return {
            "id": obj.item.id,
            "name": obj.item.name,
        }
