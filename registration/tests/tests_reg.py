import pytest

from django.urls import reverse
from knox.models import AuthToken

from rest_framework import status, exceptions

from registration.business_logic import final_creation
from registration.models import RegistrationTry, WebMenuUser
from registration.serializers import CreateRegisterTrySerializer, RegisterConfirmSerializer, WebMenuUserSerializer


class TestValidatePassword:

    def test_passwords_equal(self, randomizer):
        validated_data = randomizer.upp2_data()
        attrs = {
            'password': validated_data,
            'password2': validated_data,
        }

        result = RegisterConfirmSerializer.validate(None, attrs)
        assert result['password'] == result['password2']

    def test_passwords_different(self, randomizer):
        attrs = {
            'password': randomizer.upp2_data(),
            'password2': randomizer.upp2_data(),
        }
        # check that exception rise
        with pytest.raises(exceptions.ValidationError) as exc:
            RegisterConfirmSerializer.validate(None, attrs)
        assert "Password fields didn't match." in str(exc.value)
        assert exc.type == exceptions.ValidationError


class TestBusinessLogic:

    @pytest.mark.django_db
    def test_final_creation(self, randomizer):
        validated_data = randomizer.user()
        reg_try = RegistrationTry.objects.create(email=randomizer.email())
        result = final_creation(validated_data, reg_try)
        assert isinstance(result, WebMenuUser)
        assert result.first_name == validated_data['first_name']
        assert result.last_name == validated_data['last_name']
        assert result.email == reg_try.email
        assert result.mobile_phone == validated_data['mobile_phone']
        assert result.fathers_name == validated_data['fathers_name']
        assert result.country == validated_data['country']
        assert result.city == validated_data['city']
        assert result.street == validated_data['street']
        assert result.house_number == validated_data['house_number']
        assert result.flat_number == validated_data['flat_number']
        assert result.passport_series == validated_data['passport_series']
        assert result.passport_number == validated_data['passport_number']
        assert result.passport_date_of_issue == validated_data['passport_date_of_issue']
        assert result.passport_issuing_authority == validated_data['passport_issuing_authority']
        for_check_reg_try = RegistrationTry.objects.filter(id=reg_try.id).first()
        assert for_check_reg_try.confirmation_time is not None


class TestApiClientView:

    @pytest.mark.django_db
    def test_registration_valid_data(self, api_client, randomizer):
        url = reverse('user_reg')
        data = {
            'email': randomizer.email(),
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()  # check that response is not empty
        assert set(response.json().keys()) == set(CreateRegisterTrySerializer.Meta.fields)
        assert response.json()['email'] == response.data['email']

    @pytest.mark.django_db
    def test_registration_null_data(self, api_client):
        url = reverse('user_reg')
        data = {
            'email': None,
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()

    @pytest.mark.django_db
    def test_full_registration_valid_data(self, api_client, reg_try, randomizer):
        validated_data = randomizer.user()
        test_data = {'password': validated_data['password'],
                     'password2': validated_data['password'],
                     'first_name': validated_data['first_name'],
                     'last_name': validated_data['last_name'],
                     'fathers_name': validated_data['fathers_name'],
                     'mobile_phone': validated_data['mobile_phone'],
                     'country': validated_data['country'],
                     'city': validated_data['city'],
                     'street': validated_data['street'],
                     'house_number': validated_data['house_number'],
                     'flat_number': validated_data['flat_number'],
                     'passport_series': validated_data['passport_series'],
                     'passport_number': validated_data['passport_number'],
                     'passport_date_of_issue': validated_data['passport_date_of_issue'],
                     'passport_issuing_authority': validated_data['passport_issuing_authority'],
                     }
        data_reg_try = RegistrationTry.objects.get(email=reg_try.data['email'])
        url = reverse('registration_confirm', args=[data_reg_try.code])
        response = api_client.post(url, data=test_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()
        assert set(response.json().keys()) >= set(WebMenuUserSerializer.Meta.fields)
        assert response.json()['email'] == reg_try.data['email']
        for_check_reg_try = RegistrationTry.objects.get(id=data_reg_try.id)
        assert for_check_reg_try.confirmation_time is not None
        for_check_user = WebMenuUser.objects.get(email=reg_try.data['email'])
        assert for_check_user.first_name == validated_data['first_name']
        assert for_check_user.last_name == validated_data['last_name']
        assert for_check_user.mobile_phone == validated_data['mobile_phone']
        assert for_check_user.fathers_name == validated_data['fathers_name']
        assert for_check_user.country == validated_data['country']
        assert for_check_user.city == validated_data['city']
        assert for_check_user.street == validated_data['street']
        assert for_check_user.house_number == validated_data['house_number']
        assert for_check_user.flat_number == validated_data['flat_number']
        assert for_check_user.passport_series == validated_data['passport_series']
        assert for_check_user.passport_number == validated_data['passport_number']
        assert for_check_user.passport_date_of_issue == validated_data['passport_date_of_issue']
        assert for_check_user.passport_issuing_authority == validated_data['passport_issuing_authority']

    @pytest.mark.django_db
    def test_full_registration_reg_done_code(self, api_client, randomizer, reg_done_code):
        validated_data = randomizer.user()
        url = reverse('registration_confirm', args=[reg_done_code])
        validated_data.update({'password2': validated_data['password']})
        response = api_client.post(url, data=validated_data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()
        assert response.json()['detail'] == 'Not found.'

    @pytest.mark.django_db
    def test_full_registration_invalid_code(self, api_client, randomizer):
        validated_data = randomizer.user()
        url = reverse('registration_confirm', args=['902999ff-37d7-4125-bd84-5aaf24f1f14a'])
        validated_data.update({'password2': validated_data['password']})
        response = api_client.post(url, data=validated_data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()
        assert response.json()['detail'] == 'Not found.'


class TestKnoxView:
    @pytest.mark.django_db
    def test_login_valid_data(self, api_client, my_user_pass):
        user, password = my_user_pass
        AuthToken.objects.filter(user_id=user.id).delete()  # delete from db all tokens for user
        response = api_client.post(
            reverse('login'),
            data={
                'username': user.email,
                'password': password,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        resp_json = response.json()
        assert resp_json
        assert set(resp_json['user']) >= set(WebMenuUserSerializer.Meta.fields)
        assert resp_json['token'] is not None
        assert resp_json['expiry'] is not None
        assert AuthToken.objects.filter(user_id=user.id).exists()
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {resp_json["token"]}')
        response2 = api_client.get(reverse('user'), format='json')
        assert response2.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_login_invalid_data(self, api_client, randomizer):
        response = api_client.post(reverse('login'),
                                   data={
                                       'username': randomizer.upp2_data(),
                                       'password': randomizer.upp2_data(),
                                   }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()
        assert response.json()['non_field_errors'] == ['Access denied: wrong username or password.']

    @pytest.mark.django_db
    def test_logout(self, authenticated_client):
        client, token = authenticated_client
        response = client.post(reverse('logout'), format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not AuthToken.objects.filter(user_id=client.user.id).exists()
        response = client.get(reverse('user'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_logoutall(self, authenticated_client_2_pass):  # todo wher my problem?
        client, token, _ = authenticated_client_2_pass
        response = client.post(reverse('logoutall'), format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT  # todo it's incorrect
        assert not AuthToken.objects.filter(user_id=client.user.id).exists()
        response = client.get(reverse('user'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
