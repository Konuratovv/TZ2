from rest_framework.response import Response
from rest_framework import status
from .services import CartService, OrderService, ProductService
from rest_framework.views import APIView
from .models import Cart, Order, Product
from .serializers import CartSerializer, OrderSerializer, ProductSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

# Create your views here.

class ProductAPIView(APIView):

    """
    Весь CRUD в одной API

    """

    # permission_classes = [IsAuthenticated]
    service = ProductService()

    def post(self, request):
        data = request.data
        response_data, status_code = self.service.create_object(data)
        return Response(response_data, status=status_code)
    
    def get(self, request, pk=None):
        if pk:
            response_data, status_code = self.service.get_object(pk)
        else:
            response_data, status_code = self.service.get_all_objects()
        return Response(response_data, status=status_code)
    
    def put(self, request, pk):
        data = request.data 
        obj = self.service.get_object(pk)
        response_data, status_code = self.service.update_object(obj, data)
        return Response(response_data, status=status_code)
    
    def delete(self, request, pk):
        obj = Product.objects.get(pk=pk)
        response_data, status_code = self.service.delete_object(obj)
        return Response(response_data, status=status_code)

class ProductsFilterAPIView(generics.ListAPIView):

    """
    Список товаров по фильтрам;
    select_related - для оптимизации запросов
    
    """

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    queryset = Product.objects.select_related(
        'category'
    ).all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CartAPIView(APIView):

    """
    Корзина для товаров. Добавление и удаление в одной API

    """

    permission_classes = [IsAuthenticated]
    cart_service = CartService()

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        cart_item = self.cart_service.add_to_cart(user, product_id, quantity)
        
        return Response({'status': 'Product added to cart successfully', 'cart_item_id': cart_item.id})
    
    def delete(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        self.cart_service.remove_from_cart(user, product_id)
        return Response({"status": "Removed from cart"})
    
class CartListAPIView(generics.ListAPIView):

    """
    Просмотр товаров в корзине
    
    """

    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
class OrderAPIView(APIView):

    """
    API для оформления заказа
    
    """

    cart_service = CartService()
    order_service = OrderService()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        orders = []
        for item in cart_items:
            total_amount = self.cart_service.get_total_amount(user)
            address = request.data.get("address")
            payment_method = request.data.get("payment_method")
            order = self.cart_service.create_order_from_cart(user, item, total_amount, address, payment_method)
            orders.append(order)
        order.save()
        return Response({"status": f"Orders #{[order.id for order in orders]} have been created"})

class OrderListAPIView(generics.ListAPIView):

    """
    Просмотр заказов
    
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    
    

