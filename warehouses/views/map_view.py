from django.shortcuts import render
from dbmodels.models import ProductVariants, Inventory, Warehouses
from django.views.decorators.http import require_GET
import json

@require_GET  
def warehouse_map_view(request):
    warehouses = Warehouses.objects.all()

    variants_qs = ProductVariants.objects.all().values('id', 'variant_code')
    variants = list(variants_qs)  # Convertimos a lista para json_script

    # Datos de inventario para el mapa
    inventory_data = []
    inventories = Inventory.objects.select_related('variant__product__category', 'warehouse').all()

    for item in inventories:
        if item.variant and item.warehouse and item.quantity > 0:
            product = item.variant.product
            attributes_str = ", ".join([f"{k}: {v}" for k, v in item.variant.attributes.items()])

            inventory_data.append({
                'variant_id': item.variant.id,
                'variant_code': item.variant.variant_code,
                'variant_name': f"{product.name} - {item.variant.variant_code}",
                'price': str(item.variant.price),
                'quantity': item.quantity,
                'attributes': attributes_str,
                'product_name': product.name,
                'product_image': product.image_url or "",
                'category_name': product.category.name if product.category else "",
                'warehouse': {
                    'id': item.warehouse.id,
                    'name': item.warehouse.name,
                    'latitude': item.warehouse.coordinates.get('latitude'),
                    'longitude': item.warehouse.coordinates.get('longitude'),
                }
            })

    return render(request, 'warehouse_map.html', {
        'inventory_data': json.dumps(inventory_data),
        'variants': variants,
        'warehouses': warehouses,
    })
