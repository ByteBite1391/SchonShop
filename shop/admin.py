from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_per_page = 20

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created']
    list_filter = ['category', 'is_active', 'created']
    list_editable = ['price', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]
    list_per_page = 20
    date_hierarchy = 'created'
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'stock')
        }),
        ('تصویر و وضعیت', {
            'fields': ('image', 'is_active')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'order']
    list_filter = ['product']
    search_fields = ['product__name', 'alt_text']
    list_per_page = 20