from django.shortcuts import render
from dbmodels.models import Products
from django.views.decorators.http import require_GET

@require_GET
def catalogo_view(request):
    
    productos = Products.objects.all()
    
    return render(request, 'products/products.html', {'productos': productos})
