from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from .models import Category, Product

class HomeView(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['featured_products'] = Product.objects.filter(
            is_active=True,
            stock__gt=0
        ).select_related('category').order_by('-created')[:4]
        
        context['best_sellers'] = Product.objects.filter(
            is_active=True,
            stock__gt=0
        ).select_related('category').annotate(
            order_count=Count('order_items')
        ).order_by('-order_count', '-created')[:8]
        
        if not context['best_sellers']:
            context['best_sellers'] = Product.objects.filter(
                is_active=True,
                stock__gt=0
            ).select_related('category').order_by('-created')[:8]
        
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        
        category_slug = self.request.GET.get('category') or self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-created')
        
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['sort'] = self.request.GET.get('sort', '')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id).select_related('category')[:4]
        
        context['is_available'] = product.stock > 0
        
        return context