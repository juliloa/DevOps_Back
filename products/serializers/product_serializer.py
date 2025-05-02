# serializers.py
from rest_framework import serializers
from dbmodels.models import Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'image_url', 'category'] 
