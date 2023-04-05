from rest_framework import serializers, exceptions
from django.db import transaction

from company.models import Company
from address.models import Address

from address.serializers import AddressSerializer
from image.models import Image
from location.business_logic import validate_image_size
from location.models import Location


class LocationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    # manager = serializers.ReadOnlyField(source='manager.email')   # todo activate when manager will be

    class Meta:
        model = Location
        fields = ['company', 'id', 'legal_name', 'logo', 'address', 'phone', 'email']


class ImageSerializer(serializers.ModelSerializer):
    """Special Serializer to customize validators=[validate_image_size]"""
    image = serializers.ImageField(use_url=True, allow_null=True, validators=[validate_image_size])

    class Meta:
        model = Image
        fields = ['image']


class CreateLocationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)
    address = AddressSerializer()
    logo = ImageSerializer()

    def validate_company(self, company):
        if user := self.context.get('user'):
            if company not in user.company.all():
                raise exceptions.NotFound({"company": "Not found."})

        return company

    class Meta:
        model = Location
        fields = ['id', 'owner', 'company', 'legal_name', 'logo', 'address', 'phone', 'email', 'password']

    def create(self, validated_data):
        address_dict = validated_data.pop('address')
        logo_dict = validated_data.pop('logo')
        with transaction.atomic():  # atomic should stop other requests to db until we make the changes
            """ Works only with custom ImageSerializer. 
            Does not work directly through the serializers.ImageField."""
            location = Location.objects.create(
                address=Address.objects.create(**address_dict),
                logo=Image.objects.create(**logo_dict),
                **validated_data,
            )
        return location

    def update(self, instance, validated_data):
        address_dict = validated_data.pop('address')
        logo_dict = validated_data.pop('logo')
        # rewrite the address separately by using 'Serializer'
        instance.address = AddressSerializer().update(instance.address, address_dict)
        instance.logo = ImageSerializer().update(instance.logo, logo_dict)
        return super().update(instance, validated_data)  # rewrite company by default method - 'update'

    def validate(self, attrs):  # take from request context users password and check in database
        if user := self.context.get('user'):
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({"password": "Password incorrect."})
        attrs.pop('password')  # we must delete password for correct work serializer
        return attrs
