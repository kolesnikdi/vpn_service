from rest_framework import serializers

from Web_Menu_DA import settings
from registration.models import WebMenuUser
from two_factor_authentication.models import GoogleAuth


class Enable2faSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = WebMenuUser
        fields = ['type_2fa', 'password']

    def validate(self, attrs):  # take from request context users password and check in database
        if user := self.context.get('user'):
            if not user.check_password(attrs['password']):      # checking password
                raise serializers.ValidationError({'password': 'Password incorrect.'})
            if attrs['type_2fa'] == user.type_2fa:      # checking if such type of 2fa has been set before
                raise serializers.ValidationError({'type_2fa': 'This Choice has been enabled before.'})
        attrs.pop('password')  # we must delete password for correct work serializer
        return attrs


class GoogleAuthSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')  # change visible info from owner_id to owner_email
    # redirect_to = serializers.URLField(default=reverse('display_qr'))
    # redirect_to = serializers.URLField(default=f'{reverse("display_qr")}')
    redirect_to = serializers.URLField(default=f'{settings.HOST}/enable2fa/display_qr')

    class Meta:
        model = GoogleAuth
        fields = ['id', 'owner', 'otp_base32', 'otp_auth_url', 'redirect_to']
