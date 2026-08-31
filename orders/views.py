# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.db import transaction
from decimal import Decimal

from cart.cart import Cart
from .models import Order, OrderItem
from shop.models import Product


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


@login_required
def checkout(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'سبد خرید شما خالی است.')
        return redirect('shop:product_list')
    
    if request.method == 'POST':
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        
        if not address:
            messages.error(request, 'لطفاً آدرس خود را وارد کنید.')
            return redirect('orders:checkout')
        
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=cart.get_total_price(),
                    address=address,
                    status='pending'
                )
                
                for item in cart:
                    product = item['product']
                    
                    if product.stock < item['quantity']:
                        raise ValueError(f'موجودی محصول {product.name} کافی نیست.')
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price']
                    )
                    
                    product.stock -= item['quantity']
                    product.save()
                
                cart.clear()
                
                messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
                return redirect('orders:order_success', order_id=order.id)
                
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('cart:cart_detail')
        except Exception as e:
            messages.error(request, 'خطا در ثبت سفارش. لطفاً دوباره تلاش کنید.')
            return redirect('cart:cart_detail')
    
    context = {
        'cart': cart,
        'profile': request.user.profile if hasattr(request.user, 'profile') else None,
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})