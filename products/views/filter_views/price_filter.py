from decimal import Decimal, InvalidOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from dbmodels.models import Products
from products.serializers import ProductSerializer

class ProductPriceFilterView(APIView):

    def get(self, request):
        try:
            min_price = Decimal(request.query_params.get('min_price', '0'))
        except (InvalidOperation, TypeError):
            return Response({"error": "Invalid min_price"}, status=400)

        max_price_param = request.query_params.get('max_price')
        try:
            max_price = Decimal(max_price_param) if max_price_param else None
        except (InvalidOperation, TypeError):
            return Response({"error": "Invalid max_price"}, status=400)

        productos = Products.objects.all()
        if max_price is not None:
            productos = productos.filter(variants__price__gte=min_price, variants__price__lte=max_price)
        else:
            productos = productos.filter(variants__price__gte=min_price)

        productos = productos.distinct()
        serializer = ProductSerializer(productos, many=True)
        return Response(serializer.data)
