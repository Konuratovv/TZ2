from django.db import models
from apps.users.models import CustomUser

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    photo = models.ImageField(upload_to='products', verbose_name='Картинка', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    detailed_description = models.TextField(verbose_name='Полное описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории')
    in_stock = models.BooleanField(default=True, verbose_name="Наличие")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Feedback(models.Model):
    text = models.TextField(verbose_name='Текст')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая цена')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общее количество')
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    payment_method = models.CharField(max_length=250, verbose_name="Способ оплаты")

    
    

