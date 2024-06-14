from django.contrib import admin
from .models import Product, Cart, CartItem, Purchase, PurchaseItem


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'model',"stock"]


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

class PurcharseItemm(admin.ModelAdmin):
    list_display = ['product', 'quantity']
    list_filter = ['purchase']

admin.site.register(PurchaseItem, PurcharseItemm)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'total']
    list_filter = ['user']

admin.site.register(Purchase, PurchaseAdmin)


