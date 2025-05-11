from django.shortcuts import render, get_object_or_404, redirect
from dbmodels.models import Products, ProductVariants, Warehouses, Inventory,Categories
from django.views.decorators.http import require_GET, require_POST
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
    
@require_GET
def variant_create(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    warehouses = Warehouses.objects.all()
    return render(request, 'products/variant_form.html', {
        'product': product,
        'warehouses': warehouses
    })

@require_POST
def variant_create_post(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    variant_code = request.POST.get('variant_code')
    attributes = json.loads(request.POST.get('attributes', '{}'))  
    price = request.POST.get('price')
    warehouse_id = request.POST.get('warehouse')
    quantity = request.POST.get('quantity')

    if not variant_code or not attributes or not price or not warehouse_id or not quantity:
        return redirect('variant-create', product_id=product_id)

    variant = ProductVariants.objects.create(
        product=product,
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

@require_GET
def variant_edit_get(request, variant_id):
    variant = get_object_or_404(ProductVariants, pk=variant_id)
    inventory = Inventory.objects.filter(variant=variant).first()
    warehouses = Warehouses.objects.all()
    product = variant.product
    categories = Categories.objects.all()

    return render(request, 'products/variant_form.html', {
        'variant': variant,
        'inventory': inventory,
        'warehouses': warehouses,
        'product': product,
        'categories': categories,
    })


@require_POST
def variant_edit_post(request, variant_id):
    variant = get_object_or_404(ProductVariants, pk=variant_id)
    inventory = Inventory.objects.filter(variant=variant).first()

    variant.variant_code = request.POST.get('variant_code')
    variant.attributes = json.loads(request.POST.get('attributes'))
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

@require_POST
def variant_delete(_request, variant_id):
    variant = get_object_or_404(ProductVariants, pk=variant_id)
    product_id = variant.product_id
    variant.delete()
    return redirect('product-detail', pk=product_id)

