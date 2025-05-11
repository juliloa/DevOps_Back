from django.shortcuts import render, get_object_or_404
from dbmodels.models import Products, Categories
from django.views.decorators.http import require_GET 

@require_GET
def product_category_filter_view(request, category_id):
    categoria = get_object_or_404(Categories, pk=category_id)

    productos = Products.objects.filter(category_id=category_id)

    context = {
        'productos': productos,
        'categoria_seleccionada': categoria
    }
    return render(request, 'products/products.html', context)
