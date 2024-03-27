from django.contrib import admin
from .models import Order, Product, Category
from .models import Cart

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title'
    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'photo',
        'description',
        'detailed_description',
        'price',
        'category',
    ]

admin.site.register(Cart)
admin.site.register(Order)