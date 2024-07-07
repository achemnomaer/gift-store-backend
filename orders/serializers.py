# serializers.py
from rest_framework import serializers
from .models import Address, Order, OrderItem
from shop.serializers import SimpleProductSerializer



class OrderItemGetSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']

class OrderItemSubmissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemGetSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'updated', 'paid', 'status', 'total_amount',  'items']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"



