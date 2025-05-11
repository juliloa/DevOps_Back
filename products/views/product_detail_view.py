from django.shortcuts import render, get_object_or_404, redirect
from dbmodels.models import Products, ProductVariants,Warehouses, Inventory
import json
from django.views import View

class ProductDetailView(View):
    def get(self, request, pk):
        producto = get_object_or_404(Products, pk=pk)
        variantes = ProductVariants.objects.filter(product=producto)

        variantes_con_inventario = []
        for variante in variantes:
            inventario = Inventory.objects.filter(variant=variante).first()
            variantes_con_inventario.append({
                'id': variante.id,
                'variant_code': variante.variant_code,
                'attributes': variante.attributes,
                'price': variante.price,
                'inventory': inventario
            })

        return render(request, 'products/product_detail.html', {
            'producto': producto,
            'variantes': variantes_con_inventario
        })
    
def variant_create(request, product_id):
    if request.method == 'POST':
        variant_code = request.POST.get('variant_code')
        attributes = json.loads(request.POST.get('attributes'))
        price = request.POST.get('price')
        warehouse_id = request.POST.get('warehouse')
        quantity = request.POST.get('quantity')

        variant = ProductVariants.objects.create(
            product_id=product_id,
            variant_code=variant_code,
            attributes=attributes,
            price=price
        )

        Inventory.objects.create(
            variant=variant,
            warehouse_id=warehouse_id,
            quantity=quantity
        )

        return redirect('product-detail', pk=product_id)

    # Si la solicitud es GET, renderizamos el formulario de creación
    warehouses = Warehouses.objects.all()
    return render(request, 'products/variant_form.html', {'product_id': product_id, 'warehouses': warehouses})

def variant_edit(request, variant_id):
    variant = get_object_or_404(ProductVariants, pk=variant_id)
    inventory = Inventory.objects.filter(variant=variant).first()

    if request.method == 'POST':
        variant.variant_code = request.POST.get('variant_code')
        variant.attributes = json.loads(request.POST.get('attributes'))  # Procesa los atributos JSON
        variant.price = request.POST.get('price')
        variant.save()

        warehouse_id = request.POST.get('warehouse')
        quantity = request.POST.get('quantity')

        if inventory:
            inventory.warehouse_id = warehouse_id
            inventory.quantity = quantity
            inventory.save()
        else:
            Inventory.objects.create(
                variant=variant,
                warehouse_id=warehouse_id,
                quantity=quantity
            )

        return redirect('product-detail', pk=variant.product_id)

    warehouses = Warehouses.objects.all()
    return render(request, 'products/variant_form.html', {
        'variant': variant,
        'inventory': inventory,
        'warehouses': warehouses
    })

def variant_delete(request, variant_id):
    variant = get_object_or_404(ProductVariants, pk=variant_id)
    product_id = variant.product_id
    variant.delete()
    return redirect('product-detail', pk=product_id)
