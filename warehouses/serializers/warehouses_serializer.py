from rest_framework import serializers
from dbmodels.models import Warehouses

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouses
        fields = '__all__'
