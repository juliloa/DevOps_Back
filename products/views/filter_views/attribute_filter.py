from django.shortcuts import render
from dbmodels.models import Products
from django.db.models import Q
def product_filter_by_attributes_view(request):
    # Obtener todos los productos
    productos = Products.objects.all()

    # Obtener todos los posibles atributos de las variantes
    atributos_values = {}

    for producto in productos:
        for variant in producto.variants.all():
            if variant.attributes:  # Si el atributo existe
                for key, value in variant.attributes.items():
                    if key not in atributos_values:
                        atributos_values[key] = set()  # Usamos un set para evitar duplicados
                    atributos_values[key].add(value)

    # Convertir los valores de atributos en listas
    atributos_values = {key: list(value) for key, value in atributos_values.items()}

    # Filtrar por atributos seleccionados
    query_filter = Q()
    for atributo in atributos_values:
        value = request.GET.get(atributo)
        if value:
            query_filter &= Q(variants__attributes__contains={atributo: value})

    # Aplicamos el filtro
    if query_filter:
        productos = productos.filter(query_filter).distinct()

    return render(request, 'products/products.html', {
        'productos': productos,
        'atributos_values': atributos_values,
    })
