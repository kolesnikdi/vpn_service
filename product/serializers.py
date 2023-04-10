from rest_framework import serializers, exceptions
from django.db import transaction

from location.models import Location
from product.models import Product
from company.models import Company
from image.models import Image
from product.business_logic import validate_image_size


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'company', 'locations', 'name', 'description', 'volume', 'measure', 'cost', 'logo']


class ProductImageSerializer(serializers.ModelSerializer):
    """Special Serializer to customize validators=[validate_image_size]"""
    image = serializers.ImageField(use_url=True, allow_null=True, validators=[validate_image_size])

    class Meta:
        model = Image
        fields = ['image']


class CreateProductSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)
    locations = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=True, many=True)
    logo = ProductImageSerializer(allow_null=True,  required=False)


    def validate_company(self, company):  # todo when manager.exist make validator - if location not in user
        if user := self.context.get('user'):
            if company not in user.company.all():
                raise exceptions.NotFound({"company": "Not found."})
        return company

    class Meta:
        model = Product
        fields = ['id', 'company', 'locations', 'name', 'description', 'volume', 'measure', 'cost', 'logo']

    def create(self, validated_data):
        logo_dict = validated_data.pop('logo', None)    # for correct work we must set default None if no image in logo
        locations_list = validated_data.pop('locations')
        with transaction.atomic():
            # atomic should stop other requests to db until we make the changes
            product = Product.objects.create(
                logo=Image.objects.create(image=None),  # need to create empty logo to set company_id
                **validated_data,
            )
            # product.logo.image.save don't work if logo/image None so we need we have to rule out these options
            if logo_dict and logo_dict.get('image'):
                product.logo.image.save(f'{product.name}.jpg', logo_dict['image'])
            product.locations.set(locations_list)
        return product

    def update(self, instance, validated_data):
        logo_dict = validated_data.pop('logo')
        # make logo object separately by using custom 'Serializer'
        if logo_dict and logo_dict.get('image'):
            instance.logo.image.delete()
            instance.logo.image.save(f'{instance.name}.jpg', logo_dict['image'])
        else:
            instance.logo.image.delete()
            instance.logo = ProductImageSerializer().update(instance.logo, logo_dict)
        return super().update(instance, validated_data)  # using default method - 'update' for company
