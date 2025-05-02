
from dbmodels.models import Products
from django.shortcuts import render
from django.views import View


class ProductAttributeFilterView(View):
    def get(self, request):

        color = request.GET.get('color')
        size = request.GET.get('size')
        productos = Products.objects.all()  
        
        if color:
            productos = productos.filter(color=color)
        if size:
            productos = productos.filter(size=size)
        
        return render(request, 'product_list.html', {'productos': productos})


class ProductListView(View):
    def get(self, request):
        # Lógica para obtener y mostrar productos
        productos = Products.objects.all() 
        return render(request, 'products.html', {'productos': productos})