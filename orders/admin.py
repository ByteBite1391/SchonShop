from django.contrib import admin
from .models import Order, OrderItem


# آیتم‌ها رو به صورت جدول کنار سفارش نشون بده
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # اینا نباید دستی تغییر کنن چون تاریخچه سفارسن
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created']
    list_filter = ['status', 'created']
    # جستجو بر اساس ایمیل کاربر
    search_fields = ['user__email']
    inlines = [OrderItemInline]
    # اینا هم readonly هستن
    readonly_fields = ['total_price', 'created', 'updated']