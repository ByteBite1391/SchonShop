from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]