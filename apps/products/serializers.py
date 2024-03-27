from rest_framework import serializers

from apps.products.models import Cart, Category, Order, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product 
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart 
        fields = ['product', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "cart",
            "total_amount"
        ]
    