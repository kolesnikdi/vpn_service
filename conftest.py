import datetime

import pytest
import random
import string

from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APIClient

from company.models import Company
from address.models import Address
from image.models import Image
from location.models import Location
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

    def random_phone(self):
        """ randomize data for mobile phone"""
        return '+38063' + ''.join(random.choice(string.digits) for i in range(7))

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

    def company_data(self):
        data = {
            'legal_name': self.random_name(),
            'logo': {'image': None},  # todo upload image
            'legal_address': {'country': self.random_name(),
                              'city': self.random_name(),
                              'street': self.random_name(),
                              'house_number': self.random_digits(),
                              'flat_number': self.random_digits()},
            'actual_address': {'country': self.random_name(),
                               'city': self.random_name(),
                               'street': self.random_name(),
                               'house_number': self.random_digits(),
                               'flat_number': self.random_digits()},
            'code_USREOU': self.random_digits(),
            'phone': self.random_phone(),
            'email': self.email(),
        }
        return data

    def location_data(self):
        data = {
            'legal_name': self.random_name(),
            'logo': {'image': None},  # todo upload image
            'address': {'country': self.random_name(),
                        'city': self.random_name(),
                        'street': self.random_name(),
                        'house_number': self.random_digits(),
                        'flat_number': self.random_digits()},
            'phone': self.random_phone(),
            'email': self.email(),
        }
        return data


"""created custom users"""


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='function')  # todo don't use anywhere
def my_user(my_user_pass):
    return my_user_pass[0]


@pytest.fixture(scope='function')
def my_user_pass(django_user_model, randomizer):
    password = randomizer.upp2_data()
    user = django_user_model.objects.create_user(email=randomizer.email(), password=password)
    user.user_password = password
    return user


@pytest.fixture(scope='function')
def another_user_pass(django_user_model, randomizer):
    password = randomizer.upp2_data()
    user = django_user_model.objects.create_user(
        email=randomizer.email(),
        password=password,
        mobile_phone=randomizer.random_phone(),
    )
    user.user_password = password
    return user


@pytest.fixture(scope='function')
def authenticated_client(api_client, my_user_pass):
    api_client.user_token = AuthToken.objects.create(my_user_pass)[1]
    api_client.user = my_user_pass
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {api_client.user_token}')
    return api_client


@pytest.fixture(scope='function')
def authenticated_client_2_pass(another_user_pass):
    api_client = APIClient()
    token = AuthToken.objects.create(another_user_pass)[1]
    api_client.user_token = AuthToken.objects.create(another_user_pass)[1]
    api_client.user = another_user_pass
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {api_client.user_token}')
    return api_client


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


"""created custom company"""


@pytest.fixture(scope='function')
def custom_company(authenticated_client_2_pass, randomizer):
    company_data = randomizer.company_data()
    company = Company.objects.create(
        owner=authenticated_client_2_pass.user,
        logo=Image.objects.create(**company_data['logo']),
        legal_name=company_data['legal_name'],
        legal_address=Address.objects.create(**company_data['legal_address']),
        actual_address=Address.objects.create(**company_data['actual_address']),
        code_USREOU=company_data['code_USREOU'],
        phone=company_data['phone'],
        email=company_data['email']
    )
    company.user_password = authenticated_client_2_pass.user.user_password
    company.user = authenticated_client_2_pass
    return company

@pytest.fixture(scope='function')
def custom_location(randomizer, custom_company):
    data = randomizer.location_data()
    location = Location.objects.create(
        company=custom_company,
        logo=Image.objects.create(**data['logo']),
        legal_name=data['legal_name'],
        address=Address.objects.create(**data['address']),
        phone=data['phone'],
        email=data['email']
    )
    location.user_password = custom_company.user_password
    location.company_id = custom_company.id
    return location
