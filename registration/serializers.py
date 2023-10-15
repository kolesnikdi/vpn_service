from rest_framework import serializers
from registration.models import WebUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class LoginWebMenuUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user
        raise serializers.ValidationError('Access denied: wrong username or password.')


class WebUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = ['id', 'email', 'mobile_phone', 'first_name', 'last_name', 'fathers_name', 'country', 'city', 'street',
                  'house_number', 'flat_number', 'passport_series', 'passport_number', 'passport_date_of_issue',
                  'passport_issuing_authority']


class WebUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = ['id', 'email', 'mobile_phone', 'first_name', 'last_name', 'fathers_name', 'country', 'city', 'street',
                  'house_number', 'flat_number', 'passport_series', 'passport_number', 'passport_date_of_issue',
                  'passport_issuing_authority']

        extra_kwargs = {
            'email': {'required': False},
            'mobile_phone': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'fathers_name': {'required': False},
            'country': {'required': False},
            'city': {'required': False},
            'street': {'required': False},
            'house_number': {'required': False},
            'flat_number': {'required': False},
            'passport_series': {'required': False},
            'passport_number': {'required': False},
            'passport_date_of_issue': {'required': False},
            'passport_issuing_authority': {'required': False},
        }


class RegisterConfirmSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = WebUser
        fields = ('password', 'password2', 'email', 'mobile_phone', 'first_name', 'last_name', 'fathers_name',
                  'country', 'city', 'street', 'house_number', 'flat_number', 'passport_series', 'passport_number',
                  'passport_date_of_issue', 'passport_issuing_authority',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        attrs.pop('password2')
        return attrs
