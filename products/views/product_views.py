
from rest_framework.views import APIView
from rest_framework.response import Response
from dbmodels.models import Products
from products.serializers import ProductSerializer


class ProductListView(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)