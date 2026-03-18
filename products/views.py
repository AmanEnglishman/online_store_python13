from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Category, Review
from .forms import ReviewForm

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
    reviews = product.reviews.all().order_by('-created_at')

    form = ReviewForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('product_detail', pk=pk)


    context = {
        "product": product,
        "specifications": specifications,
        'reviews': reviews,
        'form': form
    }

    return render(request, "product_detail.html", context)

