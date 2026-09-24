# فروشگاه اینترنتی شون

پروژه فروشگاه اینترنتی با Django - مجتمع فنی تهران شعبه انقلاب

---

## نویسنده

محمد حسن خدامی

---

## تکنولوژی‌های استفاده شده

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg> Python 3.12

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5"></path><path d="M2 12l10 5 10-5"></path></svg> Django 6.1

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path><line x1="4" y1="22" x2="4" y2="15"></line></svg> django-allauth (احراز هویت با ایمیل)

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg> django-filter (فیلتر محصولات)

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg> SQLite (دیتابیس)

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg> Bootstrap 5 (فرانت‌اند)

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V4h16v3"></path><path d="M9 20h6"></path><path d="M12 4v16"></path></svg> Vazirmatn (فونت فارسی)

---

## استفاده از هوش مصنوعی

در این پروژه از ابزارهای هوش مصنوعی برای بخش‌های زیر استفاده شده است:

### 1. نوشتن lookup ها

برای نوشتن lookup های Django (مثل `__icontains`, `__gte`, `__lte` و ...) از هوش مصنوعی کمک گرفته شده است.

```python
# جستجو در نام محصول
products = products.filter(name__icontains=query)

# فیلتر قیمت
products = products.filter(price__gte=min_price)
products = products.filter(price__lte=max_price)
```

### 2. استفاده از django-filter

برای پیاده‌سازی جستجو و فیلتر محصولات از پکیج `django-filter` استفاده شده است. تنظیمات و ساختار این پکیج با کمک هوش مصنوعی انجام شده است.

### 3. فایل filters.py

فایل `filters.py` در اپ `shop` که شامل کلاس `ProductFilter` است، با کمک هوش مصنوعی نوشته شده است.

```python
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__slug')
    
    class Meta:
        model = Product
        fields = ['q', 'min_price', 'max_price', 'category']
```

### 4. استفاده از Session

برای پیاده‌سازی سبد خرید با Session، از هوش مصنوعی برای درک ساختار و نحوه استفاده از Session در Django کمک گرفته شده است.

### 5. استفاده از yield

در متد `__iter__` کلاس `Cart` از `yield` استفاده شده است. نحوه کار `yield` و Generator ها با کمک هوش مصنوعی بررسی شده است.

```python
def __iter__(self):
    product_ids = self.cart.keys()
    products = Product.objects.filter(id__in=product_ids, is_active=True)
    cart = self.cart.copy()
    
    for product in products:
        cart[str(product.id)]['product'] = product
    
    for item in cart.values():
        item['price'] = Decimal(item['price'])
        item['total_price'] = item['price'] * item['quantity']
        yield item
```

### 6. ویو cart_add و product_list

ویو `cart_add` در اپ `cart` و ویو `product_list` در اپ `shop`، با کمک هوش مصنوعی نوشته شده‌اند.

### 7. نوشتن cart/cart.py

کلاس `Cart` در فایل `cart/cart.py` که منطق سبد خرید را پیاده‌سازی می‌کند، با کمک هوش مصنوعی نوشته شده است.

### 8. کامنت‌گذاری در فایل‌ها

برای رعایت اصول clean code و کامنت‌گذاری مناسب در فایل‌ها، از هوش مصنوعی کمک گرفته شده است.

### نکته مهم

تمامی منطق اصلی پروژه (مدل‌ها، روابط بین مدل‌ها، ساختار کلی) توسط خودم طراحی و پیاده‌سازی شده است. هوش مصنوعی فقط به عنوان ابزار کمکی برای سرعت بخشیدن به توسعه و یادگیری مفاهیم جدید استفاده شده است.

---

## مفهوم Paginator در Django

### Paginator چیه؟

Paginator یعنی صفحه‌بندی (Pagination). وقتی تعداد داده‌ها زیاده، همه رو یک‌جا نمایش نمی‌دیم و تقسیمشون می‌کنیم به چند صفحه.

### مثال

فرض کن 1000 تا Post داری:

**بدون Pagination:**

```text
Post 1
Post 2
Post 3
...
Post 1000
```

**با Paginator و مثلاً 10 تا در هر صفحه:**

```text
صفحه 1 → Post 1 تا 10
صفحه 2 → Post 11 تا 20
صفحه 3 → Post 21 تا 30
...
صفحه 100 → Post 991 تا 1000
```

### مزایای Paginator

* سرعت بارگذاری صفحه بالا می‌ره
* تجربه کاربری بهتر می‌شه
* مصرف پهنای باند کم می‌شه
* دیتابیس کمتر درگیر می‌شه

### Paginator در پروژه ما

در این پروژه از Paginator برای صفحه‌بندی محصولات استفاده شده است. هر صفحه 9 محصول نمایش داده می‌شود.

**نحوه پیاده‌سازی:**

```python
from django.core.paginator import Paginator

# گرفتن همه محصولات
products = Product.objects.filter(is_active=True)

# ساخت Paginator با 9 محصول در هر صفحه
paginator = Paginator(products, 9)

# گرفتن شماره صفحه از URL
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)

# پاس دادن به template
context = {'products': page_obj, 'page_obj': page_obj}
```

**در template:**

```html
{% for product in products %}
    {{ product.name }}
{% endfor %}

{% if is_paginated %}
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">قبلی</a>
    {% endif %}
    
    صفحه {{ page_obj.number }} از {{ page_obj.paginator.num_pages }}
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">بعدی</a>
    {% endif %}
{% endif %}
```

---

## نصب و راه‌اندازی

### پیش‌نیازها

* Python 3.10 یا بالاتر
* pip

### مراحل نصب

#### 1. کلون کردن پروژه

```bash
git clone https://github.com/yourusername/shop.git
cd shop
```

#### 2. ساخت محیط مجازی

```bash
python -m venv venv
```

#### 3. فعال‌سازی محیط مجازی

**ویندوز:**

```bash
venv\Scripts\activate
```

**لینوکس/مک:**

```bash
source venv/bin/activate
```

#### 4. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

#### 5. تنظیم متغیرهای محیطی

فایل `.env.example` را به `.env` تغییر نام دهید:

**ویندوز:**

```bash
copy .env.example .env
```

**لینوکس/مک:**

```bash
cp .env.example .env
```

#### 6. اجرای migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. ساخت superuser

```bash
python manage.py createsuperuser
```

#### 8. لود کردن داده‌های نمونه

```bash
python seed_data.py
```

#### 9. اجرای پروژه

```bash
python manage.py runserver
```

سپس به آدرس:

```text
http://127.0.0.1:8000/
```

بروید.

---

## کاربران تستی

| نقش     | ایمیل                                         | رمز عبور    | توضیح                    |
| ------- | --------------------------------------------- | ----------- | ------------------------ |
| ادمین   | [admin@example.com](mailto:admin@example.com) | admin123456 | دسترسی کامل به پنل ادمین |
| کاربر 1 | [user1@example.com](mailto:user1@example.com) | user123456  | علی محمدی - 2 سفارش      |
| کاربر 2 | [user2@example.com](mailto:user2@example.com) | user123456  | زهرا احمدی - 2 سفارش     |
| کاربر 3 | [user3@example.com](mailto:user3@example.com) | user123456  | محمد کریمی - 2 سفارش     |

---

## امکانات پیاده‌سازی شده

### بخش فروشگاه

* [x] نمایش محصولات با صفحه‌بندی (9 محصول در هر صفحه)
* [x] جستجو در نام محصول
* [x] فیلتر بر اساس دسته‌بندی
* [x] فیلتر بر اساس قیمت (حداقل و حداکثر)
* [x] مرتب‌سازی (ارزان‌ترین، گران‌ترین، جدیدترین)
* [x] صفحه جزئیات محصول
* [x] نمایش محصولات مرتبط
* [x] کنترل موجودی

### سبد خرید

* [x] افزودن محصول به سبد
* [x] تغییر تعداد
* [x] حذف از سبد
* [x] محاسبه جمع کل
* [x] سبد خرید با Session (بدون نیاز به لاگین)
* [x] حفظ سبد خرید بعد از لاگین

### احراز هویت

* [x] ثبت‌نام با ایمیل
* [x] ورود با ایمیل
* [x] خروج
* [x] محافظت از صفحات با login_required

### سفارش‌ها

* [x] ثبت سفارش
* [x] کاهش موجودی بعد از ثبت
* [x] ذخیره قیمت در زمان سفارش
* [x] تاریخچه سفارش‌های کاربر
* [x] جزئیات هر سفارش
* [x] وضعیت‌های مختلف سفارش

### پنل ادمین

* [x] مدیریت دسته‌بندی‌ها
* [x] مدیریت محصولات
* [x] مدیریت تصاویر محصول
* [x] مشاهده سفارش‌ها
* [x] تغییر وضعیت سفارش
* [x] مدیریت کاربران

---

## امکاناتی که پیاده‌سازی نشده

* پرداخت آنلاین (درگاه بانکی)
* سیستم تخفیف و کوپن
* نظرات و امتیازدهی
* لیست علاقه‌مندی‌ها
* مقایسه محصولات
* REST API
* پنل فروشندگان

---

## ساختار پروژه

```text
Shop/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── filters.py
│   ├── apps.py
│   └── context_processors.py
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── cart/
│   ├── cart.py
│   ├── views.py
│   ├── urls.py
│   ├── apps.py
│   └── context_processors.py
├── orders/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fonts/
├── templates/
│   ├── base.html
│   ├── includes/
│   ├── shop/
│   ├── cart/
│   ├── orders/
│   └── accounts/
├── media/
├── manage.py
├── seed_data.py
├── requirements.txt
├── .gitignore
├── .env.example
├── LICENSE
└── README.md
```

---

## سناریوی کامل خرید

1. کاربر وارد صفحه اصلی می‌شود
2. به صفحه محصولات می‌رود
3. محصولات را مشاهده می‌کند
4. از فیلتر و جستجو استفاده می‌کند
5. به صفحه جزئیات محصول می‌رود
6. محصول را به سبد خرید اضافه می‌کند
7. سبد خرید را مشاهده می‌کند
8. تعداد را تغییر می‌دهد یا آیتم را حذف می‌کند
9. برای ثبت سفارش لاگین می‌کند
10. آدرس را وارد می‌کند
11. سفارش را ثبت می‌کند
12. پیام موفقیت می‌بیند
13. سفارش در پروفایل ثبت شده است
14. موجودی محصول کم شده است

---

## نکات فنی

### سبد خرید با Session

سبد خرید با Session پیاده‌سازی شده است. ساختار سبد به این صورت است:

```python
cart = {
    '1': {'quantity': 2, 'price': '399000'},
    '3': {'quantity': 1, 'price': '850000'}
}
```

### ذخیره قیمت در زمان سفارش

قیمت محصول در زمان سفارش در مدل `OrderItem` ذخیره می‌شود. این کار باعث می‌شود اگر بعداً قیمت محصول تغییر کند، سفارش‌های قبلی دست‌نخورده باقی بمانند.

### Transaction

از `transaction.atomic()` برای ثبت سفارش استفاده شده است. اگر خطایی رخ دهد، همه عملیات rollback می‌شود.

### CSRF Protection

از `{% csrf_token %}` در تمام فرم‌های POST استفاده شده است.

### select_related و prefetch_related

از `select_related` برای ForeignKey و `prefetch_related` برای Many-to-Many استفاده شده است تا از N+1 Query جلوگیری شود.

### POST-Redirect-GET

بعد از هر POST، یک Redirect انجام می‌شود تا از ثبت چندباره فرم با F5 جلوگیری شود.

### وضعیت‌های سفارش

| وضعیت      | توضیح            |
| ---------- | ---------------- |
| pending    | در انتظار پرداخت |
| paid       | پرداخت شده       |
| processing | در حال پردازش    |
| shipped    | ارسال شده        |
| delivered  | تحویل شده        |
| canceled   | لغو شده          |

---

## مجوز

این پروژه تحت مجوز Apache License 2.0 منتشر شده است. برای اطلاعات بیشتر به فایل [LICENSE](LICENSE) مراجعه کنید.

---

## منابع و تشکر

* [Django Documentation](https://docs.djangoproject.com/)
* [django-allauth Documentation](https://django-allauth.readthedocs.io/)
* [django-filter Documentation](https://django-filter.readthedocs.io/)
* قالب HTML: Schon
* فونت: Vazirmatn
