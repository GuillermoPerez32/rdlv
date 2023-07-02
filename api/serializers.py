from rest_framework import serializers
from .models import (Restaurant, RestaurantRating, Category,
                     Distributor, Order, Product, ProductRating, OrderDetail)
from directorio.models import User
from directorio.serializers import UserModelSerializer


class RestaurantRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRating
        fields = '__all__'


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = [
            'id',
            'user',
            'vehicle_image',
            'vehicle_id',
            'vehicle_type',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'time',
            'image',
            'category',
        ]


class RestaurantSerializer(serializers.ModelSerializer):

    user = UserModelSerializer()
    products = ProductSerializer(many=True)
    categories_product = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all(), many=True)

    def save(self, **kwargs):
        return super().save(**kwargs)

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'description',
            'address',
            'phone',
            'image',
            'user',
            'time',
            'rating',
            'products',
            'categories_product',
        ]


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'products',
            'date',
            'time',
            'address',
            'status',
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            'id',
            'order',
            'product',
            'amount',
        ]
