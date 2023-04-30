from rest_framework import serializers

from address.serializers import AddressSerializer
from location.models import Location
from product.models import Product

class ProductMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'volume', 'measure', 'cost', 'logo']


class LocationMenuSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Location
        fields = ['legal_name', 'address']
