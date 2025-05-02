
from django.shortcuts import render
from dbmodels.models import Products

def catalogo_view(request):
    
    productos = Products.objects.all()
    
    return render(request, 'products/products.html', {'productos': productos})
