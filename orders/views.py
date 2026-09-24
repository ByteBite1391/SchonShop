from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from cart.cart import Cart
from .models import Order, OrderItem


# لیست سفارش‌های کاربر
@login_required
def order_list(request):
    # فقط سفارش‌های خود کاربر رو نشون بده
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_list.html', {'orders': orders})


# جزئیات یک سفارش
@login_required
def order_detail(request, pk):
    # user=request.user برای امنیت، که کاربر سفارش بقیه رو نبینه
    order = get_object_or_404(Order, id=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


# تسویه حساب و ثبت سفارش
@login_required
def checkout(request):
    cart = Cart(request)
    
    # سبد خالی نباید ثبت بشه
    if len(cart) == 0:
        messages.warning(request, 'سبد خرید شما خالی است.')
        return redirect('shop:product_list')
    
    # کاربر فرم رو پر کرده و submit کرده
    if request.method == 'POST':
        address = request.POST.get('address', '')
        
        # آدرس خالی نباشه
        if not address:
            messages.error(request, 'لطفاً آدرس خود را وارد کنید.')
            return redirect('orders:checkout')
        
        try:
            # transaction برای اینکه اگه خطایی وسط کار پیش اومد، همه چی برگرده
            with transaction.atomic():
                # اول سفارش رو بساز
                order = Order.objects.create(
                    user=request.user,
                    total_price=cart.get_total_price(),
                    address=address,
                    status='pending'
                )
                
                # حالا آیتم‌های سفارش رو بساز
                for item in cart:
                    product = item['product']
                    
                    # چک کن موجودی کافیه
                    if product.stock < item['quantity']:
                        raise ValueError(f'موجودی {product.name} کافی نیست.')
                    
                    # قیمت رو همینجا ذخیره می‌کنیم
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price']
                    )
                    
                    # موجودی رو کم کن
                    product.stock -= item['quantity']
                    product.save()
                
                # بعد از ثبت سفارش، سبد رو خالی کن
                cart.clear()
                
                messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
                return redirect('orders:order_success', order_id=order.id)
        
        except ValueError as e:
            # خطای موجودی ناکافی
            messages.error(request, str(e))
            return redirect('cart:cart_detail')
        except Exception:
            # هر خطای دیگه
            messages.error(request, 'خطا در ثبت سفارش.')
            return redirect('cart:cart_detail')
    
    # GET: نمایش فرم تسویه حساب
    return render(request, 'orders/checkout.html', {'cart': cart})


# صفحه موفقیت سفارش
@login_required
def order_success(request, order_id):
    # فقط سفارش خود کاربر
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})