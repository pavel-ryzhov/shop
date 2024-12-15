import json

from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.models import Product, Order
from users_app.models import CustomUser

class AdminPageView(LoginRequiredMixin, TemplateView):
    template_name = "admin.html"
    login_url = 'login'

class ManageItemsView(LoginRequiredMixin, ListView):
    login_url = 'login'
    items_type = None
    template_name = 'manage_items.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_empty"] = context['object_list'].count() == 0
        context["type"] = self.items_type
        return context

class ManageUsersView(ManageItemsView):
    model = CustomUser
    items_type = "users"

class ManageProductsView(ManageItemsView):
    model = Product
    items_type = "products"

class ManageOrdersView(ManageItemsView):
    model = Order
    items_type = "orders"

class ProductView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Product
    fields = ['name', 'price', 'description']
    context_object_name = 'product'
    template_name = "view_item.html"

class UserView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = CustomUser
    fields = ['username', 'email', "phone_number", 'is_admin']
    template_name = "view_item.html"

class OrderView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Order
    context_object_name = 'order'
    template_name = "view_order.html"

class RemoveOrderView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        item_id = data.get('item_id')
        item = Order.objects.get(id=item_id)
        item.delete()
        return JsonResponse(status=200, data={'status': 'ok'})

class RemoveUserView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        item_id = data.get('item_id')
        item = CustomUser.objects.get(id=item_id)
        item.delete()
        return JsonResponse(status=200, data={'status': 'ok'})

class RemoveProductView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        item_id = data.get('item_id')
        item = Product.objects.get(id=item_id)
        item.delete()
        return JsonResponse(status=200, data={'status': 'ok'})

class AddProductView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Product
    fields = ['name', 'price', 'description']
    context_object_name = 'product'
    template_name = "add_product.html"