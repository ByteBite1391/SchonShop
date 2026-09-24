from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart


# افزودن محصول به سبد
@require_POST
def cart_add(request, product_id):
    # سبد کاربر رو می‌گیریم
    cart = Cart(request)
    
    # محصول رو از دیتابیس می‌خونیم
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # تعداد از فرم میاد، پیش‌فرض ۱
    quantity = int(request.POST.get('quantity', 1))
    
    # اگه موجودی صفر بود
    if product.stock <= 0:
        messages.error(request, 'این محصول موجود نیست.')
        return redirect('shop:product_detail', slug=product.slug)
    
    # تعداد بیشتر از موجودی نشه
    if quantity > product.stock:
        messages.warning(request, f'حداکثر موجودی {product.stock} عدد است.')
        quantity = product.stock
    
    # حالا به سبد اضافه کن
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'{product.name} به سبد خرید اضافه شد.')
    
    # برگرد به صفحه قبلی
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


# نمایش سبد خرید
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


# حذف محصول از سبد
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    
    # محصول رو بدون شرط فعال بودن می‌گیریم
    # چون کاربر باید بتونه حتی محصول غیرفعال رو هم حذف کنه
    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product)
    messages.success(request, 'محصول از سبد حذف شد.')
    return redirect('cart:cart_detail')


# تغییر تعداد محصول در سبد
@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # اگه تعداد صفر یا کمتر بود، حذفش کن
    if quantity <= 0:
        cart.remove(product)
        messages.success(request, 'محصول از سبد حذف شد.')
    else:
        # کنترل موجودی
        if quantity > product.stock:
            messages.warning(request, f'حداکثر موجودی {product.stock} عدد است.')
            quantity = product.stock
        
        # override_quantity=True یعنی تعداد جدید جایگزین قبلی بشه
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, 'سبد به‌روزرسانی شد.')
    
    return redirect('cart:cart_detail')