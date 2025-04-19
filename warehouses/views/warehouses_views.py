from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dbmodels.models import Warehouses, ProductVariants, Inventory
from warehouses.serializers import WarehouseSerializer, SimpleWarehouseSerializer

class WarehouseListView(APIView):
    def get(self, request):
        warehouses = Warehouses.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)

class WarehouseDetailView(APIView):
    def get(self, request, warehouse_id):
        try:
            warehouse = Warehouses.objects.get(id=warehouse_id)
            serializer = WarehouseSerializer(warehouse)
            return Response(serializer.data)
        except Warehouses.DoesNotExist:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        

class WarehouseByProductView(APIView):
    def get(self, request, product_id):
        inventory_qs = Inventory.objects.filter(variant__product_id=product_id).select_related('warehouse')
        warehouse_ids = inventory_qs.values_list('warehouse_id', flat=True).distinct()
        warehouses = Warehouses.objects.filter(id__in=warehouse_ids)
        serializer = SimpleWarehouseSerializer(warehouses, many=True)
        
        return Response({
            'estatus': 200,
            'message': 'todo correcto',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
