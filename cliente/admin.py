from django.contrib import admin
from .models import Product, Cart, CartItem


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'size', 'gender', 'model']
    list_filter = ['brand', 'gender']

admin.site.register(Product, ProductoAdmin)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'subtotal']
    list_filter = ['cart']

admin.site.register(CartItem, CartItemAdmin)

