from .serializers import ProductSerializer
from rest_framework import status
from .models import Product, Cart, Order


class ProductService:
    def create_object(self, data):
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data, status.HTTP_201_CREATED
    
    def get_all_objects(self):
        queryset = Product.objects.select_related('category').all()
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data, status.HTTP_200_OK
    
    def get_object(self, pk):
        try:
            obj = Product.objects.get(pk=pk)
            serializer = ProductSerializer(obj)
            return serializer.data, status.HTTP_200_OK
        except Product.DoesNotExist:
            return {'status': 'object not found'}
        
    def update_object(self, obj, data):
        serializer = ProductSerializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data, status.HTTP_200_OK
    
    def delete_object(self, obj):
        obj.delete()
        return {"message": "Object deleted successfully"}, status.HTTP_204_NO_CONTENT
    
class CartService:
    def add_to_cart(self, user, product_id, quantity=1):
        cart_item, created = Cart.objects.get_or_create(user=user, product_id=product_id)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def get_cart_items(self, user):
        return Cart.objects.select_related(
            "user",
            "product",
        ).filter(user=user)
    
    def get_total_amount(self, user):
        cart_items = self.get_cart_items(user)
        total_amount = 0
        for item in cart_items:
            total_amount += item.quantity
        return total_amount        

    def remove_from_cart(self, user, product_id):
        Cart.objects.filter(user=user, product_id=product_id).delete()

    def create_order_from_cart(self, user, cart, total_amount, address, payment_method):
        order_service = OrderService()
        order = order_service.create_order(user, cart, total_amount, address, payment_method)
        return order

class OrderService:
    def create_order(self, user, cart, total_amount, address, payment_method):
        order = Order.objects.create(
            user=user,
            cart=cart,
            total_amount=total_amount,
            address=address, 
            payment_method=payment_method
        )
        return order
    
    def get_ordered_products(self, user):
        return Order.objects.get(user=user)
        