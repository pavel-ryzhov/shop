from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from .models import Cart, CartItem, Product, Order, OrderItem
import json


class HomeView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'home.html'


class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    login_url = 'login'
    context_object_name = 'cart_items'
    template_name = 'cart.html'
    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart_id=cart.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_empty"] = context['cart_items'].count() == 0
        context["total_price"] = sum(item.total_price() for item in context['cart_items'])
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse(status=200, data={"status": "ok"})

class OrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        if cart.is_empty():
            return JsonResponse(status=404, data={"status": "fail"})
        order = Order.objects.create(user=request.user)
        for i in cart.items.all():
            OrderItem.objects.create(order=order, product=i.product, quantity=i.quantity)
        cart.delete()
        return JsonResponse(status=200, data={"status": "ok"})


class IncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        item_id = data.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
        return JsonResponse(status=200, data={
            "status": "ok",
            'quantity': cart_item.quantity,
            'item_total_price': cart_item.total_price(),
            'cart_total_price': cart_item.cart.total_price(),
        })


class DecreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        item_id = data.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        return JsonResponse(status=200, data={
            "status": "ok",
            'quantity': cart_item.quantity,
            'item_total_price': cart_item.total_price(),
            'cart_total_price': cart_item.cart.total_price(),
        })

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        item_id = data.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return JsonResponse(status=200, data={'status': 'ok', 'cart_total_price': cart_item.cart.total_price()})


class MakeOrderView(LoginRequiredMixin, ListView):
    model = CartItem
    login_url = 'login'
    context_object_name = 'cart_items'
    template_name = 'make_order.html'
    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart_id=cart.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_empty"] = context['cart_items'].count() == 0
        context["total_price"] = sum(item.total_price() for item in context['cart_items'])
        return context