from decimal import Decimal
from django.conf import settings
from shop.models import Product


# کلاس سبد خرید که توی Session ذخیره می‌شه
class Cart:
    
    # موقع ساخت، سبد رو از session می‌خونیم
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        # اگه سبد نبود، یکی جدید بساز
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    # افزودن محصول به سبد
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        
        # اگه محصول جدیده، اضافه کن
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        # یا تعداد رو جایگزین کن یا اضافه کن
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        # بیشتر از موجودی نشه
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock
        
        self.save()
    
    # ذخیره توی session
    def save(self):
        # به جنگو بگو session تغییر کرده
        self.session.modified = True
    
    # حذف محصول از سبد
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    # برای اینکه بتونیم روی سبد حلقه بزنیم
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        cart = self.cart.copy()
        
        # محصول رو به هر آیتم اضافه کن
        for product in products:
            cart[str(product.id)]['product'] = product
        
        # قیمت و جمع هر آیتم رو حساب کن
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    # تعداد کل آیتم‌ها
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    # جمع کل سبد
    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
    
    # خالی کردن سبد
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()