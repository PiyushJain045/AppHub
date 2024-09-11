from django.contrib import admin
from .models import Product, CartItem, Address
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "sold_quantity", "tag")

admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Address)
