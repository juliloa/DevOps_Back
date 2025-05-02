from django.shortcuts import render, get_object_or_404
from dbmodels.models import Products, ProductVariants
from products.serializers import ProductVariantsSerializer
from django.views import View


class ProductDetailView(View):
    def get(self, request, pk):
        producto = get_object_or_404(Products, pk=pk)
        variantes = ProductVariants.objects.filter(product=producto)

        # Usamos el serializer para obtener info con stock y warehouse
        serializer = ProductVariantsSerializer(variantes, many=True)
        return render(request, 'products/product_detail.html', {
            'producto': producto,
            'variantes': serializer.data
        })