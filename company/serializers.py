from rest_framework import serializers

from company.models import Company, Address


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    # location = serializers.PrimaryKeyRelatedField(many=True, queryset=location.objects.all()) # todo activate when locations will be
    class Meta:
        model = Company
        fields = ['owner', 'id', 'legal_name', 'legal_address', 'actual_address', 'code_USREOU', 'phone',
                  'email']  # todo add , 'location' when locations will be


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'house_number', 'flat_number']


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
        return super().update(instance, validated_data)     # rewrite company by default method - 'update'

    def validate(self, attrs):  # take from request context users password and check in database
        if user := self.context.get('user'):
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({"password": "Password incorrect."})
        attrs.pop('password')  # we must delete password for correct work serializer
        return attrs

