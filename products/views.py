from django.shortcuts import render, get_object_or_404

from .models import Product, Category

def home(request):
    products = Product.objects.prefetch_related('images').all()[:12]
    categories = Category.objects.filter(parent=None)

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'home.html', context)

def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related('images'),
        pk=pk
    )

    specifications = product.productspecification_set.all()

    context = {
        "product": product,
        "specifications": specifications
    }

    return render(request, "product_detail.html", context)