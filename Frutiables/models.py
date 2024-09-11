from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    TAG_CHOICES = [
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
    ]

    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ecom_images', null=True)
    description = models.TextField()
    sold_quantity = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} kg)"
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    default = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    company_name = models.CharField(max_length=100, null=True, blank=True) 
    address = models.TextField(null=False)  # Address cannot be null
    town_city = models.CharField(max_length=100, null=False)  # Required field
    country = models.CharField(max_length=100, null=False)  # Required field
    postcode_zip = models.CharField(max_length=20, null=False)  # Required field with a reasonable length
    mobile = models.CharField(max_length=15, null=False)  # Required field with a reasonable length

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address}"

    class Meta:
        verbose_name_plural = "Addresses"
