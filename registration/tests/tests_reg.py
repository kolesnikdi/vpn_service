import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status, exceptions

from registration.business_logic import final_creation
from registration.models import RegistrationTry
from registration.serializers import CreateRegisterTrySerializer, RegisterConfirmSerializer, UserSerializer


class TestValidatePassword:

    def test_passwords_equal(self, randomizer):
        validated_data = randomizer.upp2_data()
        attrs = {
            'password': validated_data,
            'password2': validated_data,
        }

        result = RegisterConfirmSerializer.validate(None, attrs)  # todo it wants self so I give None
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
    def test_final_creation(self, randomizer_func):
        validated_data = randomizer_func('user')
        reg_try = RegistrationTry.objects.create(email=randomizer_func('email'))
        result = final_creation(validated_data, reg_try)
        assert isinstance(result, User)
        assert result.username == validated_data['username']
        assert result.first_name == validated_data['first_name']
        assert result.last_name == validated_data['last_name']
        assert result.email == reg_try.email
        for_check_reg_try = RegistrationTry.objects.filter(id=reg_try.id).first()
        assert for_check_reg_try.confirmation_time is not None


class TestApiClientView:

    @pytest.mark.django_db
    def test_registration_valid_data(self, reg_try):
        response = reg_try
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()  # check that response is not empty
        assert set(response.json().keys()) == set(CreateRegisterTrySerializer.Meta.fields)
        assert response.json()['email'] == reg_try.data['email']

    @pytest.mark.django_db
    def test_registration_null_data(self, api_client):
        url = reverse('registration')
        data = {
            'email': None,
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()

    @pytest.mark.django_db
    def test_full_registration_valid_data(self, api_client, reg_try, randomizer):
        validated_data = randomizer.user()
        data_reg_try = RegistrationTry.objects.get(email=reg_try.data['email'])
        url = reverse('registration_confirm', args=[data_reg_try.code])
        validated_data.update({'password2': validated_data['password']})
        response = api_client.post(url, data=validated_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()
        assert set(response.json().keys()) == set(UserSerializer.Meta.fields)
        assert response.json()['username'] == validated_data['username']
        assert response.json()['email'] == reg_try.data['email']
        assert response.json()['blogs'] == []
        for_check_reg_try = RegistrationTry.objects.get(id=data_reg_try.id)
        assert for_check_reg_try.confirmation_time is not None
        for_check_user = User.objects.get(username=validated_data['username'])
        assert for_check_user.first_name == validated_data['first_name']
        assert for_check_user.last_name == validated_data['last_name']

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

