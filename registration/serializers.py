from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField

from registration.models import RegistrationTry


class RegisterConfirmSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    mobile_phone = PhoneNumberField(region="UA", required=True,max_length=13)
    country = serializers.CharField(write_only=True, required=True)
    city = serializers.CharField(write_only=True, required=True)
    street = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name', 'mobile_phone', 'country', 'city',
                  'street')
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'country': {'required': True},
            'city': {'required': True},
            'street': {'required': True},
            'mobile_phone': {'unique': True},   # todo if it correct?
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class CreateRegisterTrySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationTry
        fields = ('email',)
        extra_kwargs = {
            'email': {'required': True},
        }
