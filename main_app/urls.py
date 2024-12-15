from django.urls import path
from .views import HomeView, AddToCartView, CartView, IncreaseQuantityView, DecreaseQuantityView, RemoveFromCartView, MakeOrderView, OrderView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add_item/", AddToCartView.as_view()),
    path("cart/increase_quantity/", IncreaseQuantityView.as_view()),
    path("cart/decrease_quantity/", DecreaseQuantityView.as_view()),
    path("cart/remove_item/", RemoveFromCartView.as_view()),
    path("make_order/", MakeOrderView.as_view(), name="make_order"),
    path("make_order/order/", OrderView.as_view()),
]