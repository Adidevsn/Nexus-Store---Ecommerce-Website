from django.db import models


class Category(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='categories/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name         = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    category     = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description  = models.TextField()
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image        = models.ImageField(upload_to='products/')
    stock        = models.PositiveIntegerField(default=0)
    is_featured  = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def effective_price(self):
        return self.sale_price if self.sale_price else self.price

    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.price

    @property
    def in_stock(self):
        return self.stock > 0
