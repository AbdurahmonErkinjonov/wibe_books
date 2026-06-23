from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('accepted', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    ]
    PAYMENT_CHOICES = [
        ('naqt', 'Naqt'),
        ('karta', 'Karta'),
    ]
    DELIVERY_CHOICES = [
        ('yetkazish', 'Yetkazib berish'),
        ('olib_ketish', 'Kelib olib ketish'),
    ]

    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    extra_phone = models.CharField(max_length=20, blank=True, default='')
    telegram_username = models.CharField(max_length=200, blank=True, default='')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='naqt')
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='yetkazish')
    delivery_address = models.TextField(blank=True, default='')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.customer_name} - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} x{self.quantity}"

    class Meta:
        verbose_name_plural = "Order Items"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    pages = models.IntegerField(default=0)
    language = models.CharField(max_length=50, default="O'zbek")
    published_year = models.IntegerField(default=2024)
    isbn = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
