from django.shortcuts import render, get_object_or_404, redirect
from dbmodels.models import Products, Categories
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from django.utils.timezone import now

@require_GET
@never_cache  
def catalogo_view(request):
    
    productos = Products.objects.all()
    
    return render(request, 'products/products.html', {'productos': productos})


def product_create(request):
    if request.method == 'POST':
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
    
    categories = Categories.objects.all()
    return render(request, 'products/create.html', {'categories': categories})

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

def product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('catalogo-view')