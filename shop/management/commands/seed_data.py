from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal

from shop.models import Category, Product
from accounts.models import Profile
from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = 'ساخت داده‌های نمونه برای پروژه'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='پاک کردن داده‌های قبلی قبل از ساخت داده جدید'
        )
    
    def handle(self, *args, **options):
        if options['clean']:
            self.stdout.write(self.style.WARNING('پاک کردن داده‌های قبلی...'))
            self.clean_data()
        
        self.stdout.write(self.style.SUCCESS('شروع ساخت داده‌های نمونه...'))
        
        try:
            with transaction.atomic():
                self.create_users()
                self.create_categories()
                self.create_products()
                self.create_orders()
                
            self.show_summary()
            self.stdout.write(self.style.SUCCESS('داده‌های نمونه با موفقیت ساخته شدند.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'خطا: {str(e)}'))
            raise
    
    def clean_data(self):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('  داده‌های قبلی پاک شدند'))
    
    def create_users(self):
        self.stdout.write('\nساخت کاربران...')
        
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='user123456',
            first_name='علی',
            last_name='محمدی',
            is_active=True
        )
        self.stdout.write('  کاربر user1 ساخته شد')
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='user123456',
            first_name='زهرا',
            last_name='احمدی',
            is_active=True
        )
        self.stdout.write('  کاربر user2 ساخته شد')
        
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='user123456',
            first_name='محمد',
            last_name='کریمی',
            is_active=True
        )
        self.stdout.write('  کاربر user3 ساخته شد')
        
        Profile.objects.create(
            user=self.user1,
            phone='09123456789',
            address='تهران، خیابان آزادی، کوچه بهار، پلاک ۱۲'
        )
        Profile.objects.create(
            user=self.user2,
            phone='09351234567',
            address='تهران، خیابان ولیعصر، بالاتر از میدان ونک، پلاک ۴۵'
        )
        Profile.objects.create(
            user=self.user3,
            phone='09901234567',
            address='تهران، خیابان انقلاب، چهارراه ولیعصر، پلاک ۷۸'
        )
        self.stdout.write('  پروفایل‌ها ساخته شدند')
    
    def create_categories(self):
        self.stdout.write('\nساخت دسته‌بندی‌ها...')
        
        self.categories = {}
        
        categories_data = [
            {'name': 'مبلمان', 'slug': 'furniture'},
            {'name': 'صندلی', 'slug': 'chairs'},
            {'name': 'میز', 'slug': 'tables'},
            {'name': 'روشنایی', 'slug': 'lighting'},
            {'name': 'دکوراسیون', 'slug': 'decoration'},
        ]
        
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            self.categories[cat_data['slug']] = category
            self.stdout.write(f"  دسته‌بندی {cat_data['name']} ساخته شد")
    
    def create_products(self):
        self.stdout.write('\nساخت محصولات...')
        
        self.products = {}
        
        products_data = [
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
            {
                'name': 'صندلی قدیمی',
                'slug': 'old-chair',
                'category': 'chairs',
                'price': Decimal('150000'),
                'stock': 0,
                'description': 'این محصول غیرفعال است.',
                'is_active': False,
            },
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
        
        for prod_data in products_data:
            category = self.categories[prod_data['category']]
            product = Product.objects.create(
                category=category,
                name=prod_data['name'],
                slug=prod_data['slug'],
                price=prod_data['price'],
                stock=prod_data['stock'],
                description=prod_data['description'],
                is_active=prod_data.get('is_active', True)
            )
            self.products[prod_data['slug']] = product
            self.stdout.write(f"  محصول {prod_data['name']} ساخته شد")
    
    def create_orders(self):
        self.stdout.write('\nساخت سفارش‌های نمونه...')
        
        order1 = Order.objects.create(
            user=self.user1,
            status='delivered',
            total_price=Decimal('686000'),
            address='تهران، خیابان آزادی، کوچه بهار، پلاک ۱۲'
        )
        OrderItem.objects.create(
            order=order1,
            product=self.products['bambi-chair'],
            quantity=2,
            price=Decimal('399000')
        )
        self.stdout.write('  سفارش 1 ساخته شد (تحویل شده)')
        
        order2 = Order.objects.create(
            user=self.user1,
            status='pending',
            total_price=Decimal('2787000'),
            address='تهران، خیابان آزادی، کوچه بهار، پلاک ۱۲'
        )
        OrderItem.objects.create(
            order=order2,
            product=self.products['dining-table'],
            quantity=1,
            price=Decimal('2500000')
        )
        OrderItem.objects.create(
            order=order2,
            product=self.products['puff-chair'],
            quantity=1,
            price=Decimal('287000')
        )
        self.stdout.write('  سفارش 2 ساخته شد (در انتظار)')
        
        order3 = Order.objects.create(
            user=self.user2,
            status='processing',
            total_price=Decimal('6085000'),
            address='تهران، خیابان ولیعصر، پلاک ۴۵'
        )
        OrderItem.objects.create(
            order=order3,
            product=self.products['sofa'],
            quantity=1,
            price=Decimal('5800000')
        )
        OrderItem.objects.create(
            order=order3,
            product=self.products['puff-chair'],
            quantity=1,
            price=Decimal('287000')
        )
        self.stdout.write('  سفارش 3 ساخته شد (در حال پردازش)')
        
        order4 = Order.objects.create(
            user=self.user2,
            status='shipped',
            total_price=Decimal('1650000'),
            address='تهران، خیابان ولیعصر، پلاک ۴۵'
        )
        OrderItem.objects.create(
            order=order4,
            product=self.products['modern-chandelier'],
            quantity=1,
            price=Decimal('1650000')
        )
        self.stdout.write('  سفارش 4 ساخته شد (ارسال شده)')
        
        order5 = Order.objects.create(
            user=self.user3,
            status='canceled',
            total_price=Decimal('198000'),
            address='تهران، خیابان انقلاب، پلاک ۷۸'
        )
        OrderItem.objects.create(
            order=order5,
            product=self.products['wooden-chair'],
            quantity=1,
            price=Decimal('198000')
        )
        self.stdout.write('  سفارش 5 ساخته شد (لغو شده)')
        
        order6 = Order.objects.create(
            user=self.user3,
            status='paid',
            total_price=Decimal('3350000'),
            address='تهران، خیابان انقلاب، پلاک ۷۸'
        )
        OrderItem.objects.create(
            order=order6,
            product=self.products['desk'],
            quantity=1,
            price=Decimal('1850000')
        )
        OrderItem.objects.create(
            order=order6,
            product=self.products['table-lamp'],
            quantity=1,
            price=Decimal('450000')
        )
        OrderItem.objects.create(
            order=order6,
            product=self.products['decorative-painting'],
            quantity=1,
            price=Decimal('550000')
        )
        OrderItem.objects.create(
            order=order6,
            product=self.products['wall-mirror'],
            quantity=1,
            price=Decimal('750000')
        )
        self.stdout.write('  سفارش 6 ساخته شد (پرداخت شده)')
    
    def show_summary(self):
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('خلاصه داده‌های ساخته شده:')
        self.stdout.write('=' * 50)
        self.stdout.write(f'کاربران: {User.objects.count()}')
        self.stdout.write(f'دسته‌بندی‌ها: {Category.objects.count()}')
        self.stdout.write(f'محصولات: {Product.objects.count()}')
        self.stdout.write(f'  - فعال: {Product.objects.filter(is_active=True).count()}')
        self.stdout.write(f'  - غیرفعال: {Product.objects.filter(is_active=False).count()}')
        self.stdout.write(f'  - ناموجود: {Product.objects.filter(stock=0).count()}')
        self.stdout.write(f'سفارش‌ها: {Order.objects.count()}')
        self.stdout.write(f'آیتم‌های سفارش: {OrderItem.objects.count()}')
        self.stdout.write('=' * 50)