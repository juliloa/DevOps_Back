from django.shortcuts import render, get_object_or_404, redirect
from dbmodels.models import Products, Categories
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.cache import never_cache
from django.utils.timezone import now

@require_GET
@never_cache  
def catalogo_view(request):
    productos = Products.objects.all()

    # Simulación de atributos y sus valores, ajústalo a tu caso
    atributos_values = {
        'color': ['rojo', 'azul', 'verde'],
        'talla': ['S', 'M', 'L', 'XL'],
        'marca': ['Nike', 'Adidas', 'Puma'],
    }

    # Obtener valores seleccionados de request.GET (listas)
    atributos_seleccionados = {}
    for atributo in atributos_values.keys():
        atributos_seleccionados[atributo] = request.GET.getlist(atributo)

    contexto = {
        'productos': productos,
        'atributos_values': atributos_values,
        'atributos_seleccionados': atributos_seleccionados,
    }
    return render(request, 'products/products.html', contexto)

@require_GET
def product_create(request):
    categories = Categories.objects.all()
    return render(request, 'products/create.html', {'categories': categories})

@require_POST
def product_create_post(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    category_id = request.POST.get('category')
    image_url = request.POST.get('image_url')

    category = Categories.objects.get(id=category_id)

    product = Products(
        name=name,
        description=description,
        category=category,
        image_url=image_url,
        created_at=now()
    )
    product.save()
    return redirect('catalogo-view')

@require_GET
def product_edit_get(request, pk):
    product = get_object_or_404(Products, pk=pk)
    categories = Categories.objects.all()
    return render(request, 'products/edit.html', {
        'product': product,
        'categories': categories
    })

@require_POST
def product_edit(request, pk):
    product = get_object_or_404(Products, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        category_id = request.POST.get('category')
        product.image_url = request.POST.get('image_url')

        product.category = Categories.objects.get(id=category_id)
        product.save()
        return redirect('catalogo-view')
    
    categories = Categories.objects.all()
    return render(request, 'products/edit.html', {'product': product, 'categories': categories})

@require_POST
def product_delete(_request, pk):
    product = get_object_or_404(Products, pk=pk)
    product.delete()
    return redirect('catalogo-view')
