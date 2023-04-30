from rest_framework import viewsets, filters, generics, status

from django_filters.rest_framework import DjangoFilterBackend
from location.models import Location
from menu.filters import CustomSearchFilter, CustomRangeFilter, perform_product_filtering
from menu.serializers import LocationMenuSerializer, ProductMenuSerializer
from product.models import Product
from rest_framework.response import Response


class ProductMenuView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    pagination_class = None
    serializer_class = ProductMenuSerializer
    filter_backends = [CustomSearchFilter, CustomRangeFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'cost']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'cost', 'volume']

    def get_queryset(self):
        code = self.kwargs['code']

        return Product.objects.filter(locations__code=code).order_by('id')


class LocationMenuView(generics.RetrieveAPIView):
    PRODUCT_FILTER_BACKENDS = [CustomSearchFilter, CustomRangeFilter, filters.OrderingFilter, DjangoFilterBackend]
    """fields from Product model for search on Product level"""
    filterset_fields = ['name', 'cost']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'cost', 'volume']

    def retrieve(self, request, *args, **kwargs):
        if not (code := self.kwargs.get('code', None)):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not (location := Location.objects.filter(code=code).first()):
            return Response(status=status.HTTP_404_NOT_FOUND)
        result = LocationMenuSerializer(location).data
        location_products_qs = location.product_location.all()
        product_qs = perform_product_filtering(self, location_products_qs)
        result['products'] = ProductMenuSerializer(product_qs, many=True).data
        return Response(result, status=status.HTTP_200_OK)
