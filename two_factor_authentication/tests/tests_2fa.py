import pyotp

from django.urls import reverse
from django.core.cache import cache

from rest_framework import status

from Web_Menu_DA import settings
from Web_Menu_DA.constants import Types2FA
from two_factor_authentication.models import GoogleAuth


class Test2faEmailOnCompanyViewSet:

    def test_no_header_in_request_email_2fa(self, authenticated_client_email_2fa):
        response = authenticated_client_email_2fa.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == '2fa required'
        assert response_json['hint'] == 'Put received code into HTTP_2FACODE header and send request again.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_no_header_in_request_gauth_2fa(self, authenticated_client_email_2fa):
        authenticated_client_email_2fa.user.type_2fa = Types2FA.GAUTH
        authenticated_client_email_2fa.user.save()
        response = authenticated_client_email_2fa.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == '2fa required'
        assert response_json['hint'] == 'Put received code into HTTP_2FACODE header and send request again.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_header_is_not_valid(self, authenticated_client_email_2fa):
        cache.set(authenticated_client_email_2fa.user.id, {'code': '645987'}, 60)
        authenticated_client_email_2fa.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_client_email_2fa.user_token}',
            HTTP_2FACODE='2FACODE',
        )
        response = authenticated_client_email_2fa.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == 'Not valid 2fa data.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_header_is_valid(self, authenticated_client_email_2fa, custom_company_2):
        cache.set(authenticated_client_email_2fa.user.id, {'code': '645987'}, 60)
        authenticated_client_email_2fa.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_client_email_2fa.user_token}',
            HTTP_2FACODE='645987',
        )
        response = authenticated_client_email_2fa.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json['results']
        assert response_json['count'] == 1
        assert response.status_code == status.HTTP_200_OK

    def test_header_no_cache(self, authenticated_client_email_2fa):
        authenticated_client_email_2fa.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_client_email_2fa.user_token}',
            HTTP_2FACODE='2FACODE',
        )
        response = authenticated_client_email_2fa.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == 'Your code is already expired. Request a new one.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_header_no_authenticated(self, authenticated_client_email_2fa):
        authenticated_client_email_2fa.credentials(HTTP_2FACODE='645987')
        response = authenticated_client_email_2fa.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['detail'] == 'Authentication credentials were not provided.'
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_header_code_unfinished(self, authenticated_client_email_2fa):
        cache.set(authenticated_client_email_2fa.user.id, {'code': '645987'}, 60)
        response = authenticated_client_email_2fa.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == 'You already have unfinished 2fa confirmation.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_2fa_disabled(self, authenticated_client, custom_company_2):
        response = authenticated_client.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json['results']
        assert response_json['count'] == 1
        assert response.status_code == status.HTTP_200_OK


class TestEnable2FAView:

    def test_set_type_password_incorrect(self, authenticated_client):
        data = {'type_2fa': Types2FA.DISABLED, 'password': 'password'}
        response = authenticated_client.post(reverse('enable2fa'),data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['password'] == ['Password incorrect.']
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_incorrect_type(self, authenticated_client):
        data = {'type_2fa': 4, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['type_2fa'] == ['"4" is not a valid choice.']
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_same_type_as_it_was(self, authenticated_client):
        data = {'type_2fa': Types2FA.DISABLED, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['type_2fa'] == ['This Choice has been enabled before.']
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_type_disabled(self, authenticated_client):
        authenticated_client.user.type_2fa = Types2FA.EMAIL
        authenticated_client.user.save()
        data = {'type_2fa': Types2FA.DISABLED, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['msg'] == 'Two-factor verification successfully disabled.'
        assert response.status_code == status.HTTP_200_OK

    def test_set_type_email(self, authenticated_client):
        data = {'type_2fa': Types2FA.EMAIL, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['msg'] == 'Two-factor verification with your email successfully enabled'
        assert response.status_code == status.HTTP_200_OK

    def test_set_type_gauth(self, authenticated_client):
        data = {'type_2fa': Types2FA.GAUTH, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['msg'] == 'Two-factor verification with your Google successfully enabled.'
        data_for_check = GoogleAuth.objects.filter(owner_id=authenticated_client.user.id).last()
        assert data_for_check.owner.email == response_json['owner']
        assert data_for_check.otp_auth_url == response_json['otp_auth_url']
        assert response_json['redirect to'] == f'{settings.HOST}/enable2fa/display_qr'
        assert response.status_code == status.HTTP_200_OK

    def test_set_type_gauth_is_active_false(self, authenticated_client):
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=authenticated_client.user.email.lower(), issuer_name="Web_Menu_DA")
        data = {'type_2fa': Types2FA.GAUTH, 'password': authenticated_client.user.user_password}
        data_2fa = GoogleAuth.objects.create(owner_id=authenticated_client.user.id, otp_base32=otp_base32,
                                             otp_auth_url=otp_auth_url)
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        data_for_check = GoogleAuth.objects.get(id=data_2fa.id)
        assert data_for_check.is_active is False
        assert response.status_code == status.HTTP_200_OK


class TestDisplayQrView:

    def test_display_no_gauth_object(self, authenticated_client):
        response = authenticated_client.get(reverse('display_qr'))
        assert response
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_display_gauth_valid(self, authenticated_client_gauth_2fa):
        response = authenticated_client_gauth_2fa.get(reverse('display_qr'))
        data_for_check = GoogleAuth.objects.get(owner_id=authenticated_client_gauth_2fa.user.id)
        assert response
        assert response.data['svg']
        assert response.data['otp_base32'] == data_for_check.otp_base32
        assert data_for_check.is_hidden is True
        assert response.status_code == status.HTTP_200_OK

    def test_display_gauth_twice(self, authenticated_client_gauth_2fa):
        response = authenticated_client_gauth_2fa.get(reverse('display_qr'))
        response2 = authenticated_client_gauth_2fa.get(reverse('display_qr'))
        assert response
        assert response2
        assert response2.status_code == status.HTTP_404_NOT_FOUND

    def test_display_gauth_is_active_False(self, authenticated_client_gauth_2fa):
        gauth_object = GoogleAuth.objects.get(owner_id=authenticated_client_gauth_2fa.user.id)
        gauth_object.is_active = False
        gauth_object.save()
        response = authenticated_client_gauth_2fa.get(reverse('display_qr'))
        assert response
        assert response.status_code == status.HTTP_404_NOT_FOUND
