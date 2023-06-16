from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import filters, generics, status

from Web_Menu_DA.settings import CACHE_TIMEOUT
from location.models import Location
from menu.filters import CustomSearchFilter, CustomRangeFilter, perform_product_filtering
from menu.serializers import LocationMenuSerializer, ProductMenuSerializer


TIMEOUT = CACHE_TIMEOUT.get('LocationMenuView')

class LocationMenuView(generics.RetrieveAPIView):
    PRODUCT_FILTER_BACKENDS = [CustomSearchFilter, CustomRangeFilter, filters.OrderingFilter, DjangoFilterBackend]
    """fields from Product model for search on Product level"""
    filterset_fields = ['name', 'cost']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'cost', 'volume']

    @method_decorator(cache_page(TIMEOUT['decorator']))
    def retrieve(self, request, *args, **kwargs):
        """
        Two options for cache operation:
        1. Using a decorator (full page will be cached). Activate lines 24 and 37
        2. Using standard methods. Cache the DB request. Activate lines 38,39,40
        and deactivate lines 21 and 34
        """
        if not (code := self.kwargs.get('code', None)):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not (location := Location.objects.filter(code=code).first()):
            return Response(status=status.HTTP_404_NOT_FOUND)
        result = LocationMenuSerializer(location).data
        location_products_qs = location.product_location.all()
        # if not (location_products_qs := cache.get(code, None)):
        #     location_products_qs = location.product_location.all()
        #     cache.set(code, location_products_qs, TIMEOUT['functional'])
        product_qs = perform_product_filtering(self, location_products_qs)
        result['products'] = ProductMenuSerializer(product_qs, many=True).data
        return Response(result, status=status.HTTP_200_OK)


# class ProductMenuView(viewsets.ReadOnlyModelViewSet):
#     """Version only for serializing products. Based on viewsets with turn off pagination"""
#     queryset = Product.objects.all()
#     pagination_class = None
#     serializer_class = ProductMenuSerializer
#     filter_backends = [CustomSearchFilter, CustomRangeFilter, filters.OrderingFilter, DjangoFilterBackend]
#     filterset_fields = ['name', 'cost']
#     search_fields = ['name', 'description']
#     ordering_fields = ['name', 'cost', 'volume']
#
#     def get_queryset(self):
#         code = self.kwargs['code']
#         return Product.objects.filter(locations__code=code).order_by('id')
