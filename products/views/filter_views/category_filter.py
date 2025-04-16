
from rest_framework.views import APIView
from rest_framework.response import Response
from dbmodels.models import Products
from products.serializers import ProductSerializer

class ProductCategoryFilterView(APIView):
    def get(self, request, category_id):
        products = Products.objects.filter(category_id=category_id)
        if not products:
            return Response({"detail": "No products found for this category"}, status=404)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)