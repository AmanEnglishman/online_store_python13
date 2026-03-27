from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Category, Review
from .forms import ReviewForm

from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category


def home(request):
    products = Product.objects.prefetch_related('images').all()
    categories = Category.objects.filter(parent=None)

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    # 🔍 Поиск
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # 📂 Фильтр по категории
    if category_id:
        try:
            category = Category.objects.get(id=category_id)

            # берём все подкатегории
            subcategories = category.subcategories.all()

            products = products.filter(
                Q(category=category) |
                Q(category__in=subcategories)
            )
        except Category.DoesNotExist:
            pass


    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'query': query
    }

    return render(request, 'home.html', context)

def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related('images'),
        pk=pk
    )

    specifications = product.productspecification_set.all()
    reviews = product.reviews.all().order_by('-created_at')

    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    avg_rating = round(avg_rating, 1)

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
        'form': form,
        'avg_rating': avg_rating,
    }

    return render(request, "product_detail.html", context)