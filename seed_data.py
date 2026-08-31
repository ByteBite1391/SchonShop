# seed_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from shop.models import Category, Product
from accounts.models import Profile
from orders.models import Order, OrderItem
from decimal import Decimal

def create_seed_data():
    print("=" * 60)
    print("شروع ساخت داده‌های نمونه...")
    print("=" * 60)
    
    try:
        with transaction.atomic():
            # حذف داده‌های قبلی
            print("\n1. حذف داده‌های قبلی...")
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Profile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            print("   ✓ داده‌های قبلی حذف شدند")
            
            # ساخت کاربران
            print("\n2. ساخت کاربران...")
            user1 = User.objects.create_user(
                username='user1',
                email='user1@example.com',
                password='user123456',
                first_name='علی',
                last_name='محمدی',
                is_active=True
            )
            print("   ✓ کاربر اول ساخته شد: user1@example.com")
            
            user2 = User.objects.create_user(
                username='user2',
                email='user2@example.com',
                password='user123456',
                first_name='زهرا',
                last_name='احمدی',
                is_active=True
            )
            print("   ✓ کاربر دوم ساخته شد: user2@example.com")
            
            user3 = User.objects.create_user(
                username='user3',
                email='user3@example.com',
                password='user123456',
                first_name='محمد',
                last_name='کریمی',
                is_active=True
            )
            print("   ✓ کاربر سوم ساخته شد: user3@example.com")
            
            # ساخت پروفایل‌ها
            print("\n3. ساخت پروفایل‌ها...")
            Profile.objects.create(
                user=user1,
                phone='09123456789',
                address='تهران، خیابان آزادی، کوچه بهار، پلاک ۱۲'
            )
            Profile.objects.create(
                user=user2,
                phone='09351234567',
                address='تهران، خیابان ولیعصر، بالاتر از میدان ونک، پلاک ۴۵'
            )
            Profile.objects.create(
                user=user3,
                phone='09901234567',
                address='تهران، خیابان انقلاب، چهارراه ولیعصر، پلاک ۷۸'
            )
            print("   ✓ پروفایل‌ها ساخته شدند")
            
            # ساخت دسته‌بندی‌ها
            print("\n4. ساخت دسته‌بندی‌ها...")
            categories_data = [
                {'name': 'مبلمان', 'slug': 'furniture'},
                {'name': 'صندلی', 'slug': 'chairs'},
                {'name': 'میز', 'slug': 'tables'},
                {'name': 'روشنایی', 'slug': 'lighting'},
                {'name': 'دکوراسیون', 'slug': 'decoration'},
            ]
            
            category_objects = {}
            for cat_data in categories_data:
                category = Category.objects.create(**cat_data)
                category_objects[cat_data['slug']] = category
                print(f"   ✓ دسته‌بندی {cat_data['name']} ساخته شد")
            
            # ساخت محصولات
            print("\n5. ساخت محصولات...")
            products_data = [
                # محصولات صندلی
                {
                    'name': 'صندلی بامبی',
                    'slug': 'bambi-chair',
                    'category': 'chairs',
                    'price': Decimal('399000'),
                    'stock': 10,
                    'description': 'صندلی راحتی با طراحی مدرن و ارگونومیک. مناسب برای استفاده روزانه در منزل یا محل کار.',
                    'is_active': True,
                },
                {
                    'name': 'صندلی پاف',
                    'slug': 'puff-chair',
                    'category': 'chairs',
                    'price': Decimal('287000'),
                    'stock': 15,
                    'description': 'صندلی پاف راحتی با روکش مخمل. سبک و قابل جابجایی.',
                    'is_active': True,
                },
                {
                    'name': 'صندلی چوبی کلاسیک',
                    'slug': 'wooden-chair',
                    'category': 'chairs',
                    'price': Decimal('198000'),
                    'stock': 20,
                    'description': 'صندلی چوبی کلاسیک با طراحی زیبا و مقاوم.',
                    'is_active': True,
                },
                {
                    'name': 'صندلی مدیریتی',
                    'slug': 'office-chair',
                    'category': 'chairs',
                    'price': Decimal('1450000'),
                    'stock': 7,
                    'description': 'صندلی مدیریتی با پشتی بلند و دسته‌های قابل تنظیم.',
                    'is_active': True,
                },
                # محصولات میز
                {
                    'name': 'میز ناهارخوری',
                    'slug': 'dining-table',
                    'category': 'tables',
                    'price': Decimal('2500000'),
                    'stock': 5,
                    'description': 'میز ناهارخوری چوبی با ظرفیت ۶ نفر.',
                    'is_active': True,
                },
                {
                    'name': 'میز عسلی',
                    'slug': 'coffee-table',
                    'category': 'tables',
                    'price': Decimal('850000'),
                    'stock': 8,
                    'description': 'میز عسلی مدرن با صفحه شیشه‌ای و پایه‌های فلزی.',
                    'is_active': True,
                },
                {
                    'name': 'میز کار',
                    'slug': 'desk',
                    'category': 'tables',
                    'price': Decimal('1850000'),
                    'stock': 6,
                    'description': 'میز کار مدرن با کشوهای متعدد.',
                    'is_active': True,
                },
                # محصولات مبلمان
                {
                    'name': 'مبل راحتی سه نفره',
                    'slug': 'sofa',
                    'category': 'furniture',
                    'price': Decimal('5800000'),
                    'stock': 3,
                    'description': 'مبل راحتی سه نفره با پارچه مبلی درجه یک.',
                    'is_active': True,
                },
                {
                    'name': 'کاناپه تخت‌شو',
                    'slug': 'sofa-bed',
                    'category': 'furniture',
                    'price': Decimal('7200000'),
                    'stock': 2,
                    'description': 'کاناپه تخت‌شو با مکانیزم فلزی مقاوم.',
                    'is_active': True,
                },
                {
                    'name': 'مبل ال شکل',
                    'slug': 'l-shape-sofa',
                    'category': 'furniture',
                    'price': Decimal('9800000'),
                    'stock': 1,
                    'description': 'مبل ال شکل لوکس با پارچه ترک اعلا.',
                    'is_active': True,
                },
                # محصولات روشنایی
                {
                    'name': 'لوستر مدرن',
                    'slug': 'modern-chandelier',
                    'category': 'lighting',
                    'price': Decimal('1650000'),
                    'stock': 7,
                    'description': 'لوستر مدرن با نور LED کم مصرف.',
                    'is_active': True,
                },
                {
                    'name': 'آباژور رومیزی',
                    'slug': 'table-lamp',
                    'category': 'lighting',
                    'price': Decimal('450000'),
                    'stock': 12,
                    'description': 'آباژور رومیزی با طراحی مینیمال.',
                    'is_active': True,
                },
                {
                    'name': 'چراغ ایستاده',
                    'slug': 'floor-lamp',
                    'category': 'lighting',
                    'price': Decimal('980000'),
                    'stock': 6,
                    'description': 'چراغ ایستاده با قابلیت تنظیم ارتفاع.',
                    'is_active': True,
                },
                # محصولات دکوراسیون
                {
                    'name': 'آینه دیواری',
                    'slug': 'wall-mirror',
                    'category': 'decoration',
                    'price': Decimal('750000'),
                    'stock': 9,
                    'description': 'آینه دیواری با قاب چوبی.',
                    'is_active': True,
                },
                {
                    'name': 'تابلو دکوراتیو',
                    'slug': 'decorative-painting',
                    'category': 'decoration',
                    'price': Decimal('550000'),
                    'stock': 14,
                    'description': 'تابلو دکوراتیو با طرح انتزاعی.',
                    'is_active': True,
                },
                # محصول غیرفعال
                {
                    'name': 'صندلی قدیمی',
                    'slug': 'old-chair',
                    'category': 'chairs',
                    'price': Decimal('150000'),
                    'stock': 0,
                    'description': 'این محصول غیرفعال است.',
                    'is_active': False,
                },
                # محصول ناموجود
                {
                    'name': 'میز آنتیک',
                    'slug': 'antique-table',
                    'category': 'tables',
                    'price': Decimal('5000000'),
                    'stock': 0,
                    'description': 'میز آنتیک. این محصول ناموجود است.',
                    'is_active': True,
                },
            ]
            
            product_objects = {}
            for prod_data in products_data:
                category = category_objects[prod_data['category']]
                product = Product.objects.create(
                    category=category,
                    name=prod_data['name'],
                    slug=prod_data['slug'],
                    price=prod_data['price'],
                    stock=prod_data['stock'],
                    description=prod_data['description'],
                    is_active=prod_data.get('is_active', True)
                )
                product_objects[prod_data['slug']] = product
                print(f"   ✓ محصول {prod_data['name']} ساخته شد")
            
            # ساخت سفارش‌های نمونه
            print("\n6. ساخت سفارش‌های نمونه...")
            
            # سفارش ۱
            order1 = Order.objects.create(
                user=user1,
                status='delivered',
                total_price=Decimal('686000'),
                address='تهران، خیابان آزادی، کوچه بهار، پلاک ۱۲'
            )
            OrderItem.objects.create(
                order=order1,
                product=product_objects['bambi-chair'],
                quantity=2,
                price=Decimal('399000')
            )
            print("   ✓ سفارش ۱ ساخته شد (تحویل شده)")
            
            # سفارش ۲
            order2 = Order.objects.create(
                user=user1,
                status='pending',
                total_price=Decimal('2787000'),
                address='تهران، خیابان آزادی، کوچه بهار، پلاک ۱۲'
            )
            OrderItem.objects.create(
                order=order2,
                product=product_objects['dining-table'],
                quantity=1,
                price=Decimal('2500000')
            )
            OrderItem.objects.create(
                order=order2,
                product=product_objects['puff-chair'],
                quantity=1,
                price=Decimal('287000')
            )
            print("   ✓ سفارش ۲ ساخته شد (در انتظار)")
            
            # سفارش ۳
            order3 = Order.objects.create(
                user=user2,
                status='processing',
                total_price=Decimal('6085000'),
                address='تهران، خیابان ولیعصر، پلاک ۴۵'
            )
            OrderItem.objects.create(
                order=order3,
                product=product_objects['sofa'],
                quantity=1,
                price=Decimal('5800000')
            )
            OrderItem.objects.create(
                order=order3,
                product=product_objects['puff-chair'],
                quantity=1,
                price=Decimal('287000')
            )
            print("   ✓ سفارش ۳ ساخته شد (در حال پردازش)")
            
            # سفارش ۴
            order4 = Order.objects.create(
                user=user2,
                status='shipped',
                total_price=Decimal('1650000'),
                address='تهران، خیابان ولیعصر، پلاک ۴۵'
            )
            OrderItem.objects.create(
                order=order4,
                product=product_objects['modern-chandelier'],
                quantity=1,
                price=Decimal('1650000')
            )
            print("   ✓ سفارش ۴ ساخته شد (ارسال شده)")
            
            # سفارش ۵
            order5 = Order.objects.create(
                user=user3,
                status='canceled',
                total_price=Decimal('198000'),
                address='تهران، خیابان انقلاب، پلاک ۷۸'
            )
            OrderItem.objects.create(
                order=order5,
                product=product_objects['wooden-chair'],
                quantity=1,
                price=Decimal('198000')
            )
            print("   ✓ سفارش ۵ ساخته شد (لغو شده)")
            
            # سفارش ۶
            order6 = Order.objects.create(
                user=user3,
                status='paid',
                total_price=Decimal('3350000'),
                address='تهران، خیابان انقلاب، پلاک ۷۸'
            )
            OrderItem.objects.create(
                order=order6,
                product=product_objects['desk'],
                quantity=1,
                price=Decimal('1850000')
            )
            OrderItem.objects.create(
                order=order6,
                product=product_objects['table-lamp'],
                quantity=1,
                price=Decimal('450000')
            )
            OrderItem.objects.create(
                order=order6,
                product=product_objects['decorative-painting'],
                quantity=1,
                price=Decimal('550000')
            )
            OrderItem.objects.create(
                order=order6,
                product=product_objects['wall-mirror'],
                quantity=1,
                price=Decimal('750000')
            )
            print("   ✓ سفارش ۶ ساخته شد (پرداخت شده)")
            
            # نمایش خلاصه
            print("\n" + "=" * 60)
            print("خلاصه داده‌های ساخته شده:")
            print("=" * 60)
            print(f"👥 کاربران: {User.objects.count()}")
            print(f"📁 دسته‌بندی‌ها: {Category.objects.count()}")
            print(f"📦 محصولات: {Product.objects.count()}")
            print(f"   - فعال: {Product.objects.filter(is_active=True).count()}")
            print(f"   - غیرفعال: {Product.objects.filter(is_active=False).count()}")
            print(f"   - ناموجود: {Product.objects.filter(stock=0).count()}")
            print(f"📋 سفارش‌ها: {Order.objects.count()}")
            print(f"📝 آیتم‌های سفارش: {OrderItem.objects.count()}")
            print("=" * 60)
            print("✅ داده‌های نمونه با موفقیت ساخته شدند!")
            print("=" * 60)
            
    except Exception as e:
        print("\n❌ خطا در ساخت داده‌ها:")
        print(f"   {str(e)}")
        raise

if __name__ == '__main__':
    create_seed_data()