from django.contrib import admin
from webapp.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass