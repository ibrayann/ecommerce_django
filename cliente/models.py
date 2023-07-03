from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    # Campos adicionales si es necesario
    
    class Meta:
        app_label = 'cliente'
        swappable = 'AUTH_USER_MODEL'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='auth_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='auth_user_set',
        related_query_name='user',
    )

class Product(models.Model):
    BRAND_CHOICES = [
        ('nike', 'Nike'),
        ('adidas', 'Adidas'),
        ('puma', 'Puma'),
        # Agrega más opciones de marca según sea necesario
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    price = models.IntegerField()
    size = models.CharField(max_length=10)
    gender = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    image = models.ImageField(upload_to='productos', null=True)
    stock = models.PositiveIntegerField(default=1000)
    # Otros campos relevantes para el producto
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    @property
    def total(self):
        cart_items = self.cartitem_set.all()
        total = sum(item.subtotal for item in cart_items)
        return total

    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    @property
    def subtotal(self):
        return self.quantity * self.product.price
    # Otros campos si es necesario

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Puedes ajustar los parámetros según tus necesidades

    def __str__(self):
        return f"Purchase #{self.id}"