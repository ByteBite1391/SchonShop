import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='جستجو'
    )
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='حداقل قیمت'
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='حداکثر قیمت'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='exact',
        label='دسته‌بندی'
    )
    
    class Meta:
        model = Product
        fields = ['q', 'min_price', 'max_price', 'category']