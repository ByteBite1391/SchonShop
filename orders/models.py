from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('canceled', 'لغو شده'),
    ]
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, verbose_name="کاربر")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    total_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="جمع کل")
    address = models.TextField(verbose_name="آدرس تحویل")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ['-created']
    
    def __str__(self):
        return f"Order {self.id} - {self.user.email}"
    
    def get_status_display_fa(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت واحد")
    
    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity