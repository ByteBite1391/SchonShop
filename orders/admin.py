# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created']
    list_filter = ['status', 'created']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    inlines = [OrderItemInline]
    readonly_fields = ['total_price', 'created', 'updated']
    list_per_page = 20
    date_hierarchy = 'created'
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'address')
        }),
        ('وضعیت سفارش', {
            'fields': ('status',)
        }),
        ('مبلغ', {
            'fields': ('total_price',)
        }),
        ('تاریخ', {
            'fields': ('created', 'updated')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__status']
    search_fields = ['order__user__email', 'product__name']
    list_per_page = 20