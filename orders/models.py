from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


# مدل سفارش
class Order(models.Model):
    # وضعیت‌های ممکن سفارش
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('canceled', 'لغو شده'),
    ]
    
    # کاربری که سفارش داده
    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='کاربر'
    )
    
    # وضعیت فعلی سفارش
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت'
    )
    
    # جمع کل مبلغ سفارش
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name='جمع کل'
    )
    
    # آدرس تحویل
    address = models.TextField(verbose_name='آدرس تحویل')
    
    # تاریخ ثبت و آخرین ویرایش
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        # جدیدترین سفارش‌ها اول
        ordering = ['-created']
    
    def __str__(self):
        return f'سفارش #{self.id} - {self.user.email}'


# مدل آیتم سفارش
class OrderItem(models.Model):
    # سفارشی که این آیتم بهش تعلق داره
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='سفارش'
    )
    
    # محصولی که سفارش داده شده
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='محصول'
    )
    
    # تعداد سفارش داده شده
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    
    # قیمت محصول در زمان سفارش
    # اینجا ذخیره می‌کنیم که اگه بعداً قیمت عوض شد، سفارش قدیمی خراب نشه
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name='قیمت واحد'
    )
    
    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    # جمع جزء = قیمت × تعداد
    @property
    def subtotal(self):
        return self.price * self.quantity