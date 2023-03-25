from rest_framework import serializers, exceptions

from company.models import Address, Company
from company.serializers import AddressSerializer
from location.models import Location


class LocationSerializer(serializers.ModelSerializer):  # todo make separate application for Address
    address = AddressSerializer()
    # manager = serializers.ReadOnlyField(source='manager.email')   # todo activate when manager will be

    class Meta:
        model = Location
        fields = ['company', 'id', 'legal_name', 'logo', 'address', 'phone', 'email']


class CreateLocationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)
    address = AddressSerializer()

    def validate_company(self, company):
        if user := self.context.get('user'):
            if company not in user.company.all():
                raise exceptions.NotFound({"company": "Not found."})

        return company

    class Meta:
        model = Location
        fields = ['id', 'owner', 'company', 'legal_name', 'logo', 'address', 'phone', 'email', 'password']

    def create(self, validated_data):
        address = validated_data.pop('address')
        location = Location.objects.create(
            address=Address.objects.create(**address),
            **validated_data,
        )
        return location

    def update(self, instance, validated_data):
        address = validated_data.pop('address')
        # rewrite the address separately by using 'Serializer'
        instance.address = AddressSerializer().update(instance.address, address)
        return super().update(instance, validated_data)     # rewrite company by default method - 'update'

    def validate(self, attrs):  # take from request context users password and check in database
        if user := self.context.get('user'):
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({"password": "Password incorrect."})
        attrs.pop('password')  # we must delete password for correct work serializer
        return attrs
