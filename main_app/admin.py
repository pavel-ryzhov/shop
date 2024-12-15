from django.contrib import admin
from main_app.models import Product, Cart, CartItem, OrderItem, Order

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)