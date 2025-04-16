from django.db.models import Q
from decimal import Decimal, InvalidOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from dbmodels.models import Products, ProductVariants
from .serializers import ProductSerializer, ProductVariantsSerializer  # Cambié ProductVariantSerializer a ProductVariantsSerializer

# Tu vista se mantiene igual
class ProductListView(APIView):
    def get(self, request):
        # Obtener todos los productos
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductCategoryFilterView(APIView):
    def get(self, request, category_id):
        # Filtrar productos por categoría
        products = Products.objects.filter(category_id=category_id)
        if not products:
            return Response({"detail": "No products found for this category"}, status=404)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductWarehouseFilterView(APIView):
    def get(self, request, warehouse_id):
        # Asegurarse de filtrar correctamente a través del inventario
        products = Products.objects.filter(
            variants__inventory__warehouse_id=warehouse_id
        ).distinct()

        if not products.exists():
            return Response({"detail": "No products found in this warehouse"}, status=404)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

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

        # Filtrar productos según el rango de precio de sus variantes
        products = Products.objects.all()
        if max_price is not None:
            products = products.filter(variants__price__gte=min_price, variants__price__lte=max_price)
        else:
            products = products.filter(variants__price__gte=min_price)

        products = products.distinct()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    
class ProductAttributeFilterView(APIView):
    def get(self, request):
        # Obtener parámetros de atributos
        color = request.query_params.get('color', None)
        size = request.query_params.get('size', None)
        material = request.query_params.get('material', None)

        # Aplicar filtros condicionales
        filters = Q()
        if color:
            filters &= Q(color=color)  # Filtrar por color
        if size:
            filters &= Q(size=size)  # Filtrar por tamaño
        if material:
            filters &= Q(material=material)  # Filtrar por material

        # Obtener variantes de producto según los filtros
        variants = ProductVariants.objects.filter(filters)

        # Serializar y devolver las variantes de producto
        serializer = ProductVariantsSerializer(variants, many=True)  # Cambié ProductVariantSerializer a ProductVariantsSerializer
        return Response(serializer.data)
