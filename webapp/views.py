from django.shortcuts import render
from django.views.generic import View
from webapp.models import Product

class HomePage(View):
    def get(self, request):
        template = "main/home.html"
        products = Product.objects.all()
        ctx = {'products': products}
        return render(request, template, ctx)

