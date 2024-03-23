from django.db import models

# Create your models here.

# class Bucket(models.Model):

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    photo = models.ImageField(upload_to='products', verbose_name='Картинка')
    description = models.TextField(verbose_name='Описание')
    detailed_description = models.TextField(verbose_name='Полное описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
