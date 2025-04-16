from rest_framework import serializers
from dbmodels.models import ProductVariants, Inventory

class ProductVariantsSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    warehouse = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariants
        fields = ['id', 'attributes', 'price', 'warehouse', 'stock']

    def get_stock(self, obj):
        # Obtener el inventario relacionado con la variante
        inventory = Inventory.objects.filter(variant=obj).first()
        return inventory.quantity if inventory else 0

    def get_warehouse(self, obj):
        # Obtener la bodega asociada con la variante
        inventory = Inventory.objects.filter(variant=obj).first()
        return inventory.warehouse.name if inventory else None