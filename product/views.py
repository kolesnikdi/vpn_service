from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Web_Menu_DA.permissions import IsOwnerOr404
from product.models import Product
from product.serializers import ProductSerializer, CreateProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOr404]    #todo add permission IsManagerOr404
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Custom permission type of IsOwnerOr404.
        queryset = Product.objects.all() this one take all products
        and next one only owners products that filter through the company"""
        # todo add filter by location
        return Product.objects.filter(company__owner_id=self.request.user.id).order_by('id')
        # .order_by('id') to improve UnorderedObjectListWarning: Pagination may yield inconsistent results with
        # an unordered object_list


class CreateProductView(viewsets.ModelViewSet):
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOr404]    #todo add permission IsManagerOr404

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', {})  # if no dict in kwargs we make it
        # join user to the serializer context for opportunity def validate in CreateCompanySerializer
        kwargs['context']['user'] = self.request.user
        return super().get_serializer(*args, **kwargs)


    def get_queryset(self):
        # todo add filter by location
        return Product.objects.filter(company__owner_id=self.request.user.id).order_by('id')

