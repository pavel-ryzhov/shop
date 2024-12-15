from django.urls import path
from .views import AdminPageView, ManageUsersView, ManageProductsView, ManageOrdersView, ProductView, OrderView, \
    UserView, RemoveProductView, RemoveOrderView, RemoveUserView, AddProductView

urlpatterns = [
    path("", AdminPageView.as_view(), name="admin_page"),
    path("manage_users/", ManageUsersView.as_view(), name="manage_users"),
    path("manage_products/", ManageProductsView.as_view(), name="manage_products"),
    path("manage_orders/", ManageOrdersView.as_view(), name="manage_orders"),
    path('manage_products/<int:pk>/', ProductView.as_view()),
    path('manage_orders/<int:pk>/', OrderView.as_view()),
    path('manage_users/<int:pk>/', UserView.as_view()),
    path('manage_orders/remove_orders/', RemoveOrderView.as_view()),
    path('manage_users/remove_users/', RemoveUserView.as_view()),
    path('manage_products/remove_products/', RemoveProductView.as_view()),
    path('manage_products/add_product/', AddProductView.as_view(), name='add_product'),
]
