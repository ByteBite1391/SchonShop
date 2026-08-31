from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock <= 0:
        messages.error(request, 'این محصول موجود نیست.')
        return redirect('shop:product_detail', slug=product.slug)
    
    if quantity > product.stock:
        messages.warning(request, f'حداکثر موجودی این محصول {product.stock} عدد است.')
        quantity = product.stock
    
    cart.add(product=product, quantity=quantity, override_quantity=False)
    messages.success(request, f'{product.name} به سبد خرید اضافه شد.')
    
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, 'محصول از سبد خرید حذف شد.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart.remove(product)
        messages.success(request, 'محصول از سبد خرید حذف شد.')
    else:
        if quantity > product.stock:
            messages.warning(request, f'حداکثر موجودی این محصول {product.stock} عدد است.')
            quantity = product.stock
        
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, 'سبد خرید به‌روزرسانی شد.')
    
    return redirect('cart:cart_detail')