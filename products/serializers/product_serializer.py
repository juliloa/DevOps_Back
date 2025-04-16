from rest_framework import serializers
from dbmodels.models import Products
from .product_variant_serializer import ProductVariantsSerializer

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantsSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'category', 'image_url', 'variants']  