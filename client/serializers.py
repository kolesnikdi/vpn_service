from rest_framework import serializers
from django.contrib.auth.models import User

# from location.models import Post      # todo refactor for locations


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    # location = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())     # todo refactor for locations

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email']
        # fields = ['id', 'url', 'username', 'email', 'location']   # todo refactor for locations


class ClientSerializerPutPost(serializers.HyperlinkedModelSerializer):
    """
    Allows Admin to create new author (user). We can add new fild - 'password' to make new user with password
    """

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email']
