# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
]