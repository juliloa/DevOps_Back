from django.shortcuts import render, get_object_or_404
from dbmodels.models import Products, Warehouses
from django.views.decorators.http import require_GET 

@require_GET
def product_warehouse_filter_view(request, warehouse_id):
    warehouse = get_object_or_404(Warehouses, pk=warehouse_id)
    
    # Filtrar productos que tienen stock en esa bodega
    productos = Products.objects.filter(
        variants__inventory__warehouse_id=warehouse_id,
        variants__inventory__quantity__gt=0
    ).distinct()

    context = {
        'productos': productos,
        'bodega_seleccionada': warehouse
    }
    return render(request, 'products/products.html', context)

