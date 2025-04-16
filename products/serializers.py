from rest_framework import serializers
from dbmodels.models import Products, ProductVariants, Inventory, Categories

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


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantsSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'category', 'image_url', 'variants']  


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']
