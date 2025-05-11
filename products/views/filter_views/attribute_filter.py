from django.shortcuts import render
from dbmodels.models import Products
from django.db.models import Q
from django.views.decorators.http import require_GET 

@require_GET
def product_filter_by_attributes_view(request):
    # Obtener todos los productos
    productos = Products.objects.all()

    # Inicializar un diccionario para almacenar los valores de los atributos
    atributos_values = {}

    # Recopilar todos los valores de los atributos
    for producto in productos:
        for variant in producto.variants.all():
            if variant.attributes: 
                for key, value in variant.attributes.items():
                    atributos_values.setdefault(key, set()).add(value)

    # Convertir los valores de atributos en listas
    atributos_values = {key: list(value) for key, value in atributos_values.items()}

    # Filtrar productos según los atributos seleccionados
    query_filter = Q()
    for atributo, values in atributos_values.items():
        value = request.GET.get(atributo)
        if value:
            query_filter &= Q(variants__attributes__contains={atributo: value})

    # Aplicar el filtro si existe
    if query_filter:
        productos = productos.filter(query_filter).distinct()

    return render(request, 'products/products.html', {
        'productos': productos,
        'atributos_values': atributos_values,
    })
