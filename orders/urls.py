from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # صفحه لیست سفارش‌ها
    path('', views.order_list, name='order_list'),
    
    # صفحه تسویه حساب
    path('checkout/', views.checkout, name='checkout'),
    
    # صفحه موفقیت بعد از ثبت سفارش
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    
    # جزئیات سفارش (باید آخر باشه چون هر عددی رو می‌گیره)
    path('<int:pk>/', views.order_detail, name='order_detail'),
]