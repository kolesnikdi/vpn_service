from django.urls import reverse
from django.core.cache import cache

from rest_framework import status


class Test2faEmailOnCompanyViewSet:
    def test_no_header_in_request(self, authenticated_client):
        response = authenticated_client.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == '2fa required'
        assert response_json['hint'] == 'Put received code into HTTP_2FACODE header and send request again.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_header_is_not_valid(self, authenticated_client):
        cache.set(authenticated_client.user.id, {'code': '645987'}, 60)
        authenticated_client.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_client.user_token}',
            HTTP_2FACODE='2FACODE',
        )
        response = authenticated_client.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == 'Not valid 2fa data.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_header_is_valid(self, authenticated_client, custom_company_2):
        cache.set(authenticated_client.user.id, {'code': '645987'}, 60)
        authenticated_client.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_client.user_token}',
            HTTP_2FACODE='645987',
        )
        response = authenticated_client.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json['results']
        assert response_json['count'] == 1
        assert response.status_code == status.HTTP_200_OK

    def test_header_no_cache(self, authenticated_client, custom_company_2):
        authenticated_client.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_client.user_token}',
            HTTP_2FACODE='2FACODE',
        )
        response = authenticated_client.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == 'Your code is already expired. Request a new one.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_header_no_authenticated(self, authenticated_client, custom_company_2):
        authenticated_client.credentials(HTTP_2FACODE='645987')
        response = authenticated_client.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['detail'] == 'Authentication credentials were not provided.'
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_header_code_unfinished(self, authenticated_client, custom_company_2):
        cache.set(authenticated_client.user.id, {'code': '645987'}, 60)
        response = authenticated_client.get(reverse('company'), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['error'] == 'You already have unfinished 2fa confirmation.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST
