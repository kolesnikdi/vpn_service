from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from blog.models import Post
from registration.models import RegistrationTry


class UserSerializer(serializers.HyperlinkedModelSerializer):
    blogs = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'blogs']


class UserSerializerPutPost(serializers.HyperlinkedModelSerializer):
    """
    Allows Admin to create new author (user). We can add new fild - 'password' to make new user with password
    """

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email']


class RegisterConfirmSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
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
