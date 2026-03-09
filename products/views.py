from django.shortcuts import render

from .models import Product, Category

def home(request):
    products = Product.objects.prefetch_related('images').all()[:12]
    categories = Category.objects.filter(parent=None)

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'home.html', context)