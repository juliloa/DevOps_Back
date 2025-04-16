
from rest_framework.views import APIView
from rest_framework.response import Response
from dbmodels.models import Products
from products.serializers import ProductSerializer

class ProductWarehouseFilterView(APIView):
    def get(self, request, warehouse_id):
        products = Products.objects.filter(
            variants__inventory__warehouse_id=warehouse_id
        ).distinct()

        if not products.exists():
            return Response({"detail": "No products found in this warehouse"}, status=404)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)