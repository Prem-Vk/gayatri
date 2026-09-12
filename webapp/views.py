import time
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from webapp.models import Product, Catergory, Client
from django.conf import settings
from django.template.loader import render_to_string
from django.forms import ModelForm, forms
from django.core.mail import EmailMultiAlternatives
from django_ratelimit.decorators import ratelimit

def get_header_categories():
    cl = settings.CATEGORY_COLUMN_LENGTH
    categories = Catergory.objects.all()
    header_ctr= {
        'categories1': categories[0:cl],
        'categories2': categories[cl:cl*2],
        'categories3': categories[cl*2:cl*3],
        'all_categories': Catergory.objects.all()
    }
    return header_ctr

class HomePage(View):
    def get(self, request):
        template = "main/home.html"
        return render(request, template, get_header_categories())


class ProductPage(View):
    def get(self, request, id=0):
        template = "main/product.html"
        if id==0:
            products = Product.objects.all()
            div_id = {'div_id': 'AllProductsTab'}
        else:
            category = Catergory.objects.get(pk=int(id))
            products = Product.objects.filter(category=category)
            div_id = {'div_id': f'{category.title.replace(" ", '').replace(",", '').replace('&', '')}Tab'}
        ctx = {
            'products': products,
        }
        ctx.update(div_id)
        ctx.update(get_header_categories())
        return render(request, template, ctx)

class CategoryWiseProduct(View):
    def get(self, request, id=0):
        template = "main/category.html"
        if id==0:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category_id=int(id))
        ctx = {
            'products': products
        }
        render_html = render_to_string(template, ctx)
        return HttpResponse(render_html)


def search(request):
    template = "main/product.html"
    if request.method == 'POST':
        search_for = request.POST.get('search_for')
        products = Product.objects.filter(name__icontains=search_for)
        ctx = {
            'products': products,
            'search_for': search_for,
            'div_id': 'SearchTab',
        }
        ctx.update(get_header_categories())
        return render(request, template, ctx)

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def clean(self):
        super().clean()
        contact = self.cleaned_data.get('contact')
        if Client.objects.filter(contact=str(contact).strip()).exists():
            raise forms.ValidationError("Contact already exists!!")

def acknowledge_mail(instance: Client):
    message ='''Hi {name},

    Thank you for contacting us.
    Our team will reach you soon, on {contact}.


    Regards,
    Asgar Siddiqui
    Sales & Business Development Manager
    Gayatri Enetrprise.'''.format(name=instance.name, contact=instance.contact)
    return message

@ratelimit(key='ip', rate=settings.EMAIL_RATELIMIT)
def add_client(request):
    if request.method == 'POST':
        template = "main/home.html"
        ctx = {'show_message': True}
        ctx.update(get_header_categories())

        # 1. Honeypot check: Hidden field filled by bots, left empty by humans
        honeypot = request.POST.get('website', '').strip()
        if honeypot:
            # Bot detected: pretend success without saving or sending emails
            return render(request, template, ctx)

        # 2. Time-trap check: Forms submitted faster than 2.0s are automated bots
        form_time = request.POST.get('form_time', '').strip()
        if form_time:
            try:
                elapsed = time.time() - float(form_time)
                if elapsed < 2.0:
                    # Bot submitted too quickly
                    return render(request, template, ctx)
            except (ValueError, TypeError):
                pass

        # 3. Human submission: validate and save
        form = ClientForm(request.POST)
        if form.is_valid():
            instance: Client = form.save()

            if '@' in instance.contact and '.' in instance.contact:
                EmailMultiAlternatives(
                    'Gayatri enterpise - Acknowledgement mail',
                    f'{acknowledge_mail(instance)}',
                    settings.EMAIL_HOST_USER,
                    [f'{instance.contact}'],
                    [settings.EMAIL_HOST_USER]
                ).send()

        return render(request, template, ctx)
