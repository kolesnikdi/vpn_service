from rest_framework import serializers
from django.db import transaction

from company.models import Company
from address.models import Address
from address.serializers import AddressSerializer
from image.models import Image
from location.serializers import LocationSerializer
from company.business_logic import validate_image_size


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')  # change visible info from owner_id to owner_email
    actual_address = AddressSerializer()
    legal_address = AddressSerializer()
    location = LocationSerializer(many=True)

    class Meta:
        # ordering = ['-id']  # Need to improve UnorderedObjectListWarning:
        # Pagination may yield inconsistent results with an unordered object_list
        model = Company
        fields = ['owner', 'id', 'legal_name', 'logo', 'legal_address', 'actual_address', 'code_USREOU', 'phone',
                  'email', 'location']


class ImageSerializer(serializers.ModelSerializer):
    """Special Serializer to customize validators=[validate_image_size]"""
    image = serializers.ImageField(use_url=True, allow_null=True, validators=[validate_image_size])

    class Meta:
        model = Image
        fields = ['image']


class CreateCompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    legal_address = AddressSerializer()
    actual_address = AddressSerializer()
    logo = ImageSerializer(required=False)

    class Meta:
        model = Company
        fields = ['id', 'owner', 'legal_name', 'logo', 'legal_address', 'actual_address', 'code_USREOU', 'phone',
                  'email', 'password']

    def create(self, validated_data):
        legal_address_data = validated_data.pop('legal_address')
        actual_address_data = validated_data.pop('actual_address')
        logo_data = validated_data.pop('logo')
        company = Company.objects.create(
            legal_address=Address.objects.create(**legal_address_data),
            actual_address=Address.objects.create(**actual_address_data),
            **validated_data,
        )
        with transaction.atomic():  # atomic should stop other requests to db until we make the changes
            """ Works only with custom ImageSerializer. 
            Does not work directly through the serializers.ImageField.
            Must be created only after company.create - because we need company.id.exist
            to transfer to company_logo"""
            Image.objects.create(
                company_logo=company,
                **logo_data,
            )
        return company

    def update(self, instance, validated_data):
        legal_address_data = validated_data.pop('legal_address')
        actual_address_data = validated_data.pop('actual_address')
        logo_data = validated_data.pop('logo')
        # rewrite the address separately by using 'Serializer'
        instance.legal_address = AddressSerializer().update(instance.legal_address, legal_address_data)
        instance.actual_address = AddressSerializer().update(instance.actual_address, actual_address_data)
        instance.logo = ImageSerializer().update(instance.logo, logo_data)
        return super().update(instance, validated_data)  # rewrite company by default method - 'update'

    def validate(self, attrs):  # take from request context users password and check in database
        if user := self.context.get('user'):
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({"password": "Password incorrect."})
        attrs.pop('password')  # we must delete password for correct work serializer
        return attrs
