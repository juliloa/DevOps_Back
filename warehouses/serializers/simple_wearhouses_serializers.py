from dbmodels.models import Warehouses
from rest_framework import serializers

class SimpleWarehouseSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='name')
    latitud = serializers.SerializerMethodField()
    longitud = serializers.SerializerMethodField()

    class Meta:
        model = Warehouses
        fields = ['nombre', 'latitud', 'longitud']

    def get_latitud(self, obj):
        return obj.coordinates.get('latitude') if obj.coordinates else None

    def get_longitud(self, obj):
        return obj.coordinates.get('longitude') if obj.coordinates else None
