from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from dbmodels.models import Products

def product_price_filter_view(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    try:
        min_price = Decimal(min_price) if min_price else Decimal('0')
    except (InvalidOperation, TypeError):
        min_price = Decimal('0')

    try:
        max_price = Decimal(max_price) if max_price else None
    except (InvalidOperation, TypeError):
        max_price = None

    productos = Products.objects.all()
    if max_price is not None:
        productos = productos.filter(variants__price__gte=min_price, variants__price__lte=max_price)
    else:
        productos = productos.filter(variants__price__gte=min_price)

    productos = productos.distinct()

    context = {
        'productos': productos,
        'min_price': min_price,
        'max_price': max_price
    }
    return render(request, 'products/products.html', context)
