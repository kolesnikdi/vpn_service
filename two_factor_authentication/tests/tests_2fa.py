import pyotp
import pytest

from django.urls import reverse
from django.core.cache import cache

from rest_framework import status

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
        authenticated_client_email_2fa.user.type_2fa = 2
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
        data = {'type_2fa': 0, 'password': 'password'}
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
        data = {'type_2fa': 0, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['type_2fa'] == ['This Choice has been enabled before.']
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_type_disabled(self, authenticated_client):
        authenticated_client.user.type_2fa = 1
        authenticated_client.user.save()
        data = {'type_2fa': 0, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['msg'] == 'Two-factor verification successfully disabled.'
        assert response.status_code == status.HTTP_200_OK

    def test_set_type_email(self, authenticated_client):
        data = {'type_2fa': 1, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['msg'] == 'Two-factor verification with your email successfully enabled'
        assert response.status_code == status.HTTP_200_OK

    def test_set_type_gauth(self, authenticated_client):
        data = {'type_2fa': 2, 'password': authenticated_client.user.user_password}
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['msg'] == 'Two-factor verification with your Google successfully enabled.'
        data_for_check = GoogleAuth.objects.filter(owner_id=authenticated_client.user.id).last()
        assert data_for_check.owner.email == response_json['owner']
        assert data_for_check.otp_auth_url == response_json['otp_auth_url']
        assert response_json['warning'] == f'Write down or make a copy of the token {data_for_check.otp_base32}.' \
                                           f' You won\'t see it again.'
        assert response.status_code == status.HTTP_200_OK

    def test_set_type_gauth_is_active_false(self, authenticated_client):
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=authenticated_client.user.email.lower(), issuer_name="Web_Menu_DA")
        data = {'type_2fa': 2, 'password': authenticated_client.user.user_password}
        data_2fa = GoogleAuth.objects.create(owner_id=authenticated_client.user.id, otp_base32=otp_base32,
                                             otp_auth_url=otp_auth_url)
        response = authenticated_client.post(reverse('enable2fa'), data=data, format='json')
        response_json = response.json()
        assert response_json
        data_for_check = GoogleAuth.objects.get(id=data_2fa.id)
        assert data_for_check.is_active is False
        assert response.status_code == status.HTTP_200_OK


class TestDisplayQrView:

    def test_(self, authenticated_client):
        from django.test.client import MULTIPART_CONTENT, BOUNDARY, CONTENT_TYPE_RE, JSON_CONTENT_TYPE_RE
        # response = authenticated_client.get(reverse('display_qr'), format='multipart')
        # response = authenticated_client.get('/display_qr', content_type='text/html', charset='utf-8')
        # response = authenticated_client.get('/display_qr')
        response = authenticated_client.get(reverse('display_qr'), content_type=MULTIPART_CONTENT)
        response_json = response.json()
        data_for_check = GoogleAuth.objects.get(id=authenticated_client.user.id)
        assert response_json
        assert response.status_code == status.HTTP_200_OK
