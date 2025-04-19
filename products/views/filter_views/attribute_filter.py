from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from dbmodels.models import ProductVariants
from products.serializers import ProductVariantsSerializer  


class ProductAttributeFilterView(APIView):
    def get(self, request):
        color = request.query_params.get('color', None)
        size = request.query_params.get('size', None)
        material = request.query_params.get('material', None)

        filters = Q()
        if color:
            filters &= Q(attributes__color=color)
        if size:
            filters &= Q(attributes__size=size)
        if material:
            filters &= Q(attributes__material=material)

        variants = ProductVariants.objects.filter(filters)
        serializer = ProductVariantsSerializer(variants, many=True)
        return Response(serializer.data)
