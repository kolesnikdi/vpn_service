from django.urls import reverse

from rest_framework import status

from product.models import Product


class TestValidators:

    def test_location_incorrect(self, custom_location, custom_company_2, randomizer):
        data = randomizer.product_data()
        data['company'] = custom_company_2.id
        data['locations'] = [custom_location.id]
        response = custom_location.user.post(reverse('product_new-list'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_json['company'] == 'Company does not found.'

    def test_location_defunct(self, custom_location, randomizer):
        data = randomizer.product_data()
        data['company'] = custom_location.company.id
        data['locations'] = [custom_location.id + 10]
        response = custom_location.user.post(reverse('product_new-list'), data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()
        assert response_json
        assert response_json['locations'] == ['Invalid pk "11" - object does not exist.']

    def test_company_defunct(self, custom_location, randomizer):
        data = randomizer.product_data()
        data['company'] = custom_location.company.id + 10
        data['locations'] = [custom_location.id]
        response = custom_location.user.post(reverse('product_new-list'), data=data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_json = response.json()
        assert response_json
        assert response_json['object'] == 'Location or/and Company does not found.'


class TestCreateProductView:
    def test_create_product_valid(self, custom_location, randomizer):
        data = randomizer.product_data()
        data['locations'] = [custom_location.id]
        data['company'] = custom_location.company.id
        old_products_ids = list(Product.objects.all().values_list('id', flat=True))  # check if old notes exist
        # flat=True - makes one list from tuple lists
        response = custom_location.user.post(reverse('product_new-list'), data=data, format='json')
        assert response.json()
        assert response.status_code == status.HTTP_201_CREATED
        # if old notes exist we exclude(id__in=old_products_ids) them from QuerySet
        product_qs = Product.objects.filter(locations__in=[custom_location.id]).exclude(id__in=old_products_ids)
        assert product_qs
        assert product_qs.count() == 1
        for_check_create_product = product_qs.last()
        assert for_check_create_product.name == data['name']
        assert not bool(for_check_create_product.logo.image)  # true if not False=bool((for_check_create_location.logo)
        assert for_check_create_product.description == data['description']
        assert for_check_create_product.measure == data['measure']
        assert str(for_check_create_product.volume) in data['volume']
        assert str(for_check_create_product.cost)[:4] in data['cost']
        assert for_check_create_product.created_date is not None
        assert for_check_create_product.locations
        assert for_check_create_product.company_id == data['company']

    def test_update_product_valid(self, randomizer, custom_product, custom_location):
        data = randomizer.product_data()
        data['locations'] = [custom_location.id]
        data['company'] = custom_location.company.id
        old_products_ids = list(Product.objects.all().values_list('id', flat=True))  # check if old notes exist
        assert old_products_ids
        assert len(old_products_ids) == 1
        url = reverse('product_new-detail', kwargs={'pk': custom_product.id})
        response = custom_location.user.put(url, data=data, format='json')
        assert response.json()
        assert response.status_code == status.HTTP_200_OK
        for_check_update_product = Product.objects.get(id=custom_product.id)
        assert for_check_update_product.name == data['name']
        assert not bool(for_check_update_product.logo.image)
        assert for_check_update_product.description == data['description']
        assert str(for_check_update_product.volume) in data['volume']
        assert for_check_update_product.measure == data['measure']
        assert str(for_check_update_product.cost)[:4] in data['cost']

    def test_delete_product(self, custom_product, custom_location):
        response = custom_location.user.delete(reverse('product_new-detail', kwargs={'pk': custom_product.id}))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_product_another_client(self, authenticated_client, custom_product):
        response = authenticated_client.delete(reverse('product_new-detail', kwargs={'pk': custom_product.id}))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_product_another_client(self, authenticated_client, custom_product, randomizer):
        data = randomizer.product_data()
        data['locations'] = [custom_product.location_id]
        data['company'] = custom_product.company.id
        url = reverse('product_new-detail', kwargs={'pk': custom_product.id})
        response = authenticated_client.put(url, data=data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()


class TestProductViewSet:
    def test_product_view_owner(self, authenticated_client_2_pass, custom_product):
        response = authenticated_client_2_pass.get(reverse('product'), format='json')
        response_json = response.json()
        assert response_json
        data = response_json['results'][0]
        assert response.status_code == status.HTTP_200_OK
        assert custom_product.company_id == data['company']
        assert custom_product.locations
        assert custom_product.name == data['name']
        assert custom_product.created_date is not None
        assert custom_product.description == data['description']
        assert str(data['volume']) in custom_product.volume
        assert custom_product.measure == data['measure']
        assert data['cost'][:4] in custom_product.cost

    def test_product_view_pk_anoter_user(self, authenticated_client, custom_product):
        url = reverse('product_new-detail', kwargs={'pk': custom_product.id})
        response = authenticated_client.get(url, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()
