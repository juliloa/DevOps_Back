from django.views.generic import ListView
from dbmodels.models import Products
from django.http import Http404

class ProductCategoryFilterView(ListView):
    model = Products
    template_name = 'products/category_filter.html'  
    context_object_name = 'productos'
    
    def get_queryset(self):
        category_id = self.kwargs['category_id'] 
        productos = Products.objects.filter(category_id=category_id)
        if not productos:
            raise Http404("No products found for this category")
        return productos
