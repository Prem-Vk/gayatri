from django.contrib import admin
from webapp.models import Product, Catergory, Client
from django.contrib.auth.models import Group, User


admin.site.unregister(Group)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Catergory)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass
