from rest_framework import serializers

from company.models import Company
from address.models import Address
from address.serializers import AddressSerializer
from location.serializers import LocationSerializer


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


class CreateCompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    legal_address = AddressSerializer()
    actual_address = AddressSerializer()

    class Meta:
        model = Company
        fields = ['id', 'owner', 'legal_name', 'logo', 'legal_address', 'actual_address', 'code_USREOU', 'phone',
                  'email', 'password']

    def create(self, validated_data):
        legal_address = validated_data.pop('legal_address')
        actual_address = validated_data.pop('actual_address')
        company = Company.objects.create(
            legal_address=Address.objects.create(**legal_address),
            actual_address=Address.objects.create(**actual_address),
            **validated_data,
        )
        return company

    def update(self, instance, validated_data):
        legal_address = validated_data.pop('legal_address')
        actual_address = validated_data.pop('actual_address')
        # rewrite the address separately by using 'Serializer'
        instance.legal_address = AddressSerializer().update(instance.legal_address, legal_address)
        instance.actual_address = AddressSerializer().update(instance.actual_address, actual_address)
        return super().update(instance, validated_data)  # rewrite company by default method - 'update'

    def validate(self, attrs):  # take from request context users password and check in database
        if user := self.context.get('user'):
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({"password": "Password incorrect."})
        attrs.pop('password')  # we must delete password for correct work serializer
        return attrs
