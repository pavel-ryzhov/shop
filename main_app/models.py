from django.db.models import Model, CharField, FloatField, TextField, ForeignKey, CASCADE, OneToOneField, PositiveIntegerField
from django.urls import reverse
from django.conf import settings

class Product(Model):
    name = CharField(max_length=100)
    description = TextField()
    price = FloatField()
    def __str__(self):
        return self.name
    @staticmethod
    def get_absolute_url():
        return reverse("manage_products")

class Cart(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True, related_name="cart")
    def __str__(self):
        return f"{self.user}'s cart"
    def is_empty(self):
        return self.items.count() == 0
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name="items")
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    def total_price(self):
        return self.product.price * self.quantity


class Order(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="orders")
    def __str__(self):
        return f"{self.user}'s order {self.id}"
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    @staticmethod
    def get_absolute_url():
        return reverse("manage_orders")

class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name="items")
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    def total_price(self):
        return self.product.price * self.quantity

