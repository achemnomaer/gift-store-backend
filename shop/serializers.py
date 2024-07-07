from rest_framework import serializers

from .models import (Category, Occasion, Product, RecipientType, Review)


# Category serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# occassion serializer
class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = "__all__"


# recipient type serializer
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientType
        fields = "__all__"



# Simple Product Serializer
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "product_image", "price", "discounted_price"]



# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_average_rating(self, obj):
        return obj.average_rating()


# serializers for review
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


# Product serializer for search
class ProductSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "product_image",
                  "price", "discounted_price")
