import datetime

import pytest
import random
import string

from knox.models import AuthToken
from rest_framework.test import APIClient


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

    def random_digits_limit(self, limit):
        """ randomize digits"""
        digit = '123456789'
        return ''.join(random.choice(digit) for i in range(limit))


"""created custom users"""
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='function')
def user(django_user_model, randomizer):
    password = randomizer.upp2_data()
    user = django_user_model.objects.create_user(
        id=randomizer.random_digits_limit(3),
        email=randomizer.email(),
        password=password
    )
    user.user_password = password
    return user


@pytest.fixture(scope='function')
def authenticated_client(api_client, user):
    api_client.user_token = AuthToken.objects.create(user)[1]
    api_client.user = user
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {api_client.user_token}')
    return api_client
