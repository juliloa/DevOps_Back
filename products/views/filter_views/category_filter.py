from django.shortcuts import render, get_object_or_404
from dbmodels.models import Products, Categories

def product_category_filter_view(request, category_id):
    categoria = get_object_or_404(Categories, pk=category_id)

    productos = Products.objects.filter(category_id=category_id)

    context = {
        'productos': productos,
        'categoria_seleccionada': categoria
    }
    return render(request, 'products/products.html', context)
