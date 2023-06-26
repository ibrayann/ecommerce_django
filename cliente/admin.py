from django.contrib import admin
from .models import Product


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'size', 'gender', 'model']
    list_filter = ['brand', 'gender']

admin.site.register(Product, ProductoAdmin)