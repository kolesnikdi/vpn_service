from rest_framework import serializers

from product.models import Product


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'volume', 'measure', 'cost', 'logo')

