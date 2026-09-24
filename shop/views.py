from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .filters import ProductFilter


# صفحه اصلی سایت
def home(request):
    # ۴ محصول آخر که موجودی دارن
    featured_products = Product.objects.filter(
        is_active=True,
        stock__gt=0
    ).order_by('-created')[:4]
    
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'shop/home.html', context)


# لیست محصولات + جستجو + فیلتر
def product_list(request, category_slug=None):
    # همه محصولات فعال
    products = Product.objects.filter(is_active=True)
    
    # دسته بندی در آدرس (url)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # انجام فیلتر ها با django-filter
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    
    # مرتب سازی
    sort = request.GET.get('sort')
    if sort == 'price_asc': # گرفتن محصولات از کم به زیاد
        products = products.order_by('price')
    elif sort == 'price_desc': # گرفتن محصولات از زیاد به کم
        products = products.order_by('-price')
    else: # گرفتن محصولات بر اساس زمان ایجاد (زودتر)
        products = products.order_by('-created')
    
    # شماره صفحه رو از URL می‌گیریم
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1
        
    # ادامه با ai نوشته شده است
    
    # محاسبه شروع و پایان برای slicing
    per_page = 9
    total = products.count()
    start = (page_number - 1) * per_page
    end = start + per_page
    products_page = products[start:end]
    
    # تعداد کل صفحات با فرمول سقف
    total_pages = (total + per_page - 1) // per_page
    has_previous = page_number > 1
    has_next = page_number < total_pages
    
    context = {
        'products': products_page,
        'filter': product_filter,
        'categories': Category.objects.all(),
        'current_category': category_slug,
        'sort': sort or '',
        'page_number': page_number,
        'total_pages': total_pages,
        'has_previous': has_previous,
        'has_next': has_next,
        'previous_page': page_number - 1,
        'next_page': page_number + 1,
    }
    return render(request, 'shop/product_list.html', context)


# صفحه جزئیات محصول
def product_detail(request, slug):
    # فقط محصول فعال رو نشون بده
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # محصولات همون دسته، بدون خودش
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)