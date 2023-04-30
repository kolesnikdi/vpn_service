import uuid

from django.urls import reverse

from rest_framework import status


class TestValidateMenu:

    def test_get_menu_positive(self, api_client, custom_location, custom_products_for_filtering):
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json['legal_name']
        assert response_json['address']
        assert len(response_json['products']) == 10

    def test_get_menu_wrong_code(self, api_client, custom_location, custom_product):
        response = api_client.get(reverse('list_menu', args=[uuid.uuid4()]), format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_menu_post(self, api_client, custom_location, custom_product):
        response = api_client.post(reverse('list_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_menu_patch(self, api_client, custom_location, custom_product):
        response = api_client.patch(reverse('list_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_menu_delete(self, api_client, custom_location, custom_product):
        response = api_client.delete(reverse('list_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestValidateSearchFilter:

    def test_menu_filter_search_positive(self, api_client, custom_location, custom_products_for_filtering):
        search_query = custom_products_for_filtering[1]
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'search={search_query.name}'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json['legal_name']
        assert response_json['address']
        assert len(response_json['products']) == 1

    def test_menu_filter_invalid_search(self, api_client, custom_location, custom_products_for_filtering):
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'search={custom_products_for_filtering[0].name[:2]}'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json
        assert response_json['legal_name']
        assert response_json['address']
        assert len(response_json['products']) == 10

class TestValidateOrderingFilter:
    def test_menu_filter_reverse_ordering_positive(self, api_client, custom_location, custom_products_for_filtering):
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': 'ordering=-cost'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()['products']
        assert response_json
        assert response_json[0]['cost'] > response_json[2]['cost']

    def test_menu_filter_ordering_positive(self, api_client, custom_location, custom_products_for_filtering):
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': 'ordering=volume'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()['products']
        assert response_json
        assert response_json[0]['volume'] < response_json[2]['volume']


class TestValidateFiltersetFilter:
    def test_menu_filterset_positive(self, api_client, custom_location, custom_products_for_filtering):
        search_query = custom_products_for_filtering[2]
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'name={search_query.name}&cost={search_query.cost}'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 1

    def test_menu_filterset_invalid(self, api_client, custom_location, custom_products_for_filtering):
        search_query = custom_products_for_filtering[2]
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'name={search_query.name[2:]}&cost={search_query.cost[:2]}'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json == []
        assert response.status_code == status.HTTP_200_OK


class TestValidateRangeFilter:
    def test_menu_filter_range_one_param_to_end(self, api_client, custom_location, custom_products_for_filtering):
        """from the specified parameter to the end"""
        custom_products_for_filtering.sort(key=lambda x: x.cost)
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={custom_products_for_filtering[2].cost},'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 8
        assert custom_products_for_filtering[1].cost + '.00' not in [x['cost'] for x in response_json]
        assert custom_products_for_filtering[2].cost + '.00' in [x['cost'] for x in response_json]
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_beginning_to_param(self, api_client, custom_location, custom_products_for_filtering):
        """from beginning to the specified parameter"""
        custom_products_for_filtering.sort(key=lambda x: x.cost)
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost=,{custom_products_for_filtering[7].cost}'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 8
        assert custom_products_for_filtering[8].cost + '.00' not in [x['cost'] for x in response_json]
        assert custom_products_for_filtering[7].cost + '.00' in [x['cost'] for x in response_json]
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_param_to_param(self, api_client, custom_location, custom_products_for_filtering):
        """from the specified parameter to the specified parameter"""
        custom_products_for_filtering.sort(key=lambda x: x.cost)
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={custom_products_for_filtering[5].cost},'
                               f'{custom_products_for_filtering[6].cost}'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 2
        assert custom_products_for_filtering[4].cost + '.00' not in [x['cost'] for x in response_json]
        assert custom_products_for_filtering[5].cost + '.00' in [x['cost'] for x in response_json]
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_several_param(self, api_client, custom_location, custom_products_for_filtering):
        """ filter by several fields simultaneously """
        custom_products_for_filtering.sort(key=lambda x: x.cost)
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={custom_products_for_filtering[5].cost},'
                               f'{custom_products_for_filtering[7].cost}'
                               f'&range_volume={custom_products_for_filtering[5]},{custom_products_for_filtering[6]}'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) <= 3
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_invalid_name_param(self, api_client, custom_location, custom_products_for_filtering):
        custom_products_for_filtering.sort(key=lambda x: x.cost)
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'rng_cost={custom_products_for_filtering[0].cost},'
                               f'{custom_products_for_filtering[1].cost}'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 10
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_invalid_param_value(self, api_client, custom_location, custom_products_for_filtering):
        """ invalid parameter - no coma after first value """
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={custom_products_for_filtering[8].cost}'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 10
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_invalid_field_name(self, api_client, custom_location, custom_products_for_filtering):
        """ invalid parameter name - range_name """
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_name={custom_products_for_filtering[8].name},'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 10
        assert response.status_code == status.HTTP_200_OK


class TestSeveralFilter:
    def test_menu_filter_range_and_ordering(self, api_client, custom_location, custom_products_for_filtering):
        """ from the specified parameter to the specified parameter
        from largest to smallest """
        custom_products_for_filtering.sort(key=lambda x: x.cost)
        response = api_client.get(
            reverse('list_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={custom_products_for_filtering[2].cost}'
                               f',{custom_products_for_filtering[9].cost}'
                               f'&ordering=-cost'},
            format='json',
        )
        response_json = response.json()['products']
        assert response_json
        assert len(response_json) == 8
        assert response_json[0]['cost'] > response_json[1]['cost']
        assert response.status_code == status.HTTP_200_OK
