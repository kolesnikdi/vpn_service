from django.urls import reverse

from rest_framework import status

from address.models import Address
from location.models import Location


class TestValidateCompany:

    def test_passwords_incorrect(self, custom_company, randomizer):
        data = randomizer.location_data()
        data['password'] = custom_company.user_password
        data['company'] = custom_company.id + 10
        response = custom_company.user.post(reverse('location_new-list'), data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()
        assert response_json
        assert response_json['company'] == ['Invalid pk "11" - object does not exist.']


class TestCreateLocationView:
    def test_create_location_valid(self, custom_company, randomizer):
        data = randomizer.location_data()
        data['password'] = custom_company.user_password
        data['company'] = custom_company.id
        response = custom_company.user.post(reverse('location_new-list'), data=data, format='json')
        assert response.json()
        assert response.status_code == status.HTTP_201_CREATED
        for_check_create_location = Location.objects.get(company_id=custom_company.id)
        assert for_check_create_location.legal_name == data['legal_name']
        assert not bool(for_check_create_location.logo.image)  # true if not False=bool((for_check_create_location.logo)
        assert for_check_create_location.address_id is not None
        assert for_check_create_location.phone == data['phone']
        assert for_check_create_location.email == data['email']
        assert for_check_create_location.created_date is not None
        for_check_create_address = Address.objects.get(id=for_check_create_location.address_id)
        assert for_check_create_address.country == data['address']['country']
        assert for_check_create_address.city == data['address']['city']
        assert for_check_create_address.street == data['address']['street']
        assert for_check_create_address.house_number == data['address']['house_number']
        assert for_check_create_address.flat_number == data['address']['flat_number']

    def test_update_location_valid(self, randomizer, custom_company, custom_location):
        data = randomizer.location_data()
        data['password'] = custom_company.user_password
        data['company'] = custom_company.id
        url = reverse('location_new-detail', kwargs={'pk': custom_location.id})
        response = custom_company.user.put(url, data=data, format='json')
        assert response.json()
        assert response.status_code == status.HTTP_200_OK
        for_check_update_location = Location.objects.get(id=custom_location.id)
        assert for_check_update_location.legal_name == data['legal_name']
        assert not bool(for_check_update_location.logo.image)
        assert for_check_update_location.address  # true if address exist
        assert for_check_update_location.address_id is not None
        assert for_check_update_location.phone == data['phone']
        assert for_check_update_location.email == data['email']
        assert for_check_update_location.created_date is not None
        for_check_update_address = Address.objects.get(id=for_check_update_location.address_id)
        assert for_check_update_address.country == data['address']['country']
        assert for_check_update_address.city == data['address']['city']
        assert for_check_update_address.street == data['address']['street']
        assert for_check_update_address.house_number == data['address']['house_number']
        assert for_check_update_address.flat_number == data['address']['flat_number']

    def test_delete_location(self, custom_company, custom_location):
        response = custom_company.user.delete(reverse('location_new-detail', kwargs={'pk': custom_location.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_location_another_client(self, authenticated_client, custom_location):
        response = authenticated_client.delete(reverse('location_new-detail', kwargs={'pk': custom_location.id}))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_location_another_client(self, authenticated_client, custom_location, randomizer):
        data = randomizer.location_data()
        data.setdefault('password', custom_location.user_password)
        data.setdefault('company', custom_location.company_id)
        url = reverse('location_new-detail', kwargs={'pk': custom_location.id})
        response = authenticated_client.put(url, data=data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()


class TestLocationViewSet:
    def test_location_view_owner(self, authenticated_client_2_pass, custom_location):
        response = authenticated_client_2_pass.get(reverse('location'), format='json')
        response_json = response.json()
        assert response_json
        data = response_json['results'][0]
        assert response.status_code == status.HTTP_200_OK
        assert custom_location.company_id == data['company']
        assert custom_location.legal_name == data['legal_name']
        assert custom_location.address is not None
        assert custom_location.phone == data['phone']
        assert custom_location.email == data['email']

    def test_location_view_pk_anoter_user(self, authenticated_client, custom_location):
        url = reverse('location_new-detail', kwargs={'pk': custom_location.id})
        response = authenticated_client.get(url, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()
