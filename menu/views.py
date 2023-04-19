from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from menu.filters import CustomSearchFilter, CustomRangeFilter
from menu.serializers import MenuSerializer
from product.models import Product


class MenuView(viewsets.ReadOnlyModelViewSet):
    serializer_class = MenuSerializer
    filter_backends = [CustomSearchFilter, filters.OrderingFilter, DjangoFilterBackend, CustomRangeFilter]
    filterset_fields = ['name', 'cost']
    search_fields = ['name', 'description']
    ordering_fields = ['cost', 'volume']

    def get_queryset(self):
        code = self.kwargs['code']
        return Product.objects.filter(locations__code=code).order_by('id')
