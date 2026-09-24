from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='دسته‌بندی'
    )
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت')
    stock = models.PositiveIntegerField(verbose_name='موجودی')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])
    
    @property
    def is_available(self):
        return self.is_active and self.stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='محصول'
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='تصویر')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='متن جایگزین')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    
    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصول'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.product.name} - {self.id}'