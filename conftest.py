import datetime

import pytest
import random
import string

from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APIClient

from registration.models import RegistrationTry

"""randomizers"""


@pytest.fixture(scope='function')
def randomizer():
    return Randomizer()


class Randomizer:

    def email(self):
        """ randomize data for email"""
        return ''.join(random.choice(string.hexdigits) for i in range(10)) + "@gmail.com"

    def upp2_data(self):
        """ randomize data for username, password, password2"""
        return ''.join(random.choice(string.hexdigits) for i in range(10))

    def random_name(self):
        """ randomize data for first_name, last_name"""
        return ''.join(random.choice(string.ascii_letters) for i in range(10)).title()

    def user(self):
        """ randomize data user"""
        user = {
            'username': None,
            'first_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'last_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'password': ''.join(random.choice(string.hexdigits) for i in range(10)),
            'mobile_phone': '+38063' + ''.join(random.choice(string.digits) for i in range(7)),
            'fathers_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'country': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'city': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'street': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'house_number': ''.join(random.choice(string.digits) for i in range(2)),
            'flat_number': ''.join(random.choice(string.digits) for i in range(2)),
            'passport_series': ''.join(random.choice(string.ascii_letters) for i in range(2)).title(),
            'passport_number': ''.join(random.choice(string.digits) for i in range(6)),
            'passport_date_of_issue': datetime.date.today(),
            'passport_issuing_authority': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'is_staff': False,
            'is_active': True,
            'date_joined': datetime.datetime.now(),
        }
        return user

    def random_digits(self):
        """ randomize digits"""
        return ''.join(random.choice(string.digits) for i in range(10))


"""created custom users"""


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='function')
def my_user_pass(django_user_model, randomizer):
    password = randomizer.upp2_data()
    user = django_user_model.objects.create_user(email=randomizer.email(), password=password)
    return user, password


@pytest.fixture(scope='function')
def authenticated_client(api_client, my_user_pass):
    token = AuthToken.objects.create(my_user_pass[0])[1]
    api_client.user = my_user_pass[0]

    return api_client, token  # return api_client with authenticated user (like method)


@pytest.fixture(scope='function')
def authenticated_client_2(api_client, my_user_pass):
    # api_client.credentials(Authorization=f'Token {token2}')
    token = AuthToken.objects.create(my_user_pass[0])[1]
    token2 = AuthToken.objects.create(my_user_pass[0])[1]
    api_client.user = my_user_pass[0]
    return api_client, token


"""fixture for registration app"""


@pytest.fixture
def reg_try(randomizer, api_client):
    url = reverse('user_reg')
    data = {
        'email': randomizer.email(),
    }
    response = api_client.post(url, data=data, format='json')
    return response


@pytest.fixture
def reg_done_code(api_client, reg_try, randomizer):
    validated_data = randomizer.user()
    data_reg_try = RegistrationTry.objects.get(email=reg_try.data['email'])
    url = reverse('registration_confirm', args=[data_reg_try.code])
    validated_data.update({'password2': validated_data['password']})
    api_client.post(url, data=validated_data, format='json')
    for_check_reg_try = RegistrationTry.objects.get(id=data_reg_try.id)
    return for_check_reg_try.code
