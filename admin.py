from django.contrib import admin

# Register your models here.
from cart.models import Cart, CartItem


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'cart', 'quantity', 'active']


admin.site.register(CartItem, CartItemAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']


admin.site.register(Cart, CartAdmin)
