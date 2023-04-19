from django.urls import reverse

from rest_framework import status


class TestValidateMenu:

    def test_menu_exist(self, api_client, custom_location, custom_product):
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()['results'][0]
        assert response_json
        assert response_json['id'] == custom_product.id
        assert response_json['name'] == custom_product.name
        assert response_json['description'] == custom_product.description
        assert response_json['volume'] == int(custom_product.volume)
        assert response_json['measure'] == custom_product.measure
        assert custom_product.cost in response_json['cost']
        assert response_json['logo'] is not None

    def test_menu_post(self, api_client, custom_location, custom_product):
        response = api_client.post(reverse('display_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_menu_patch(self, api_client, custom_location, custom_product):
        response = api_client.patch(reverse('display_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_menu_delete(self, api_client, custom_location, custom_product):
        response = api_client.delete(reverse('display_menu', args=[custom_location.code]), format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

class TestValidateSearchFilter:

    def test_menu_filter_search(self, api_client, custom_location, custom_products_for_filtering):
        search_query = custom_products_for_filtering[1]
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'search={search_query.name}'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()['results'][0]
        assert response_json
        assert response_json['id'] == search_query.id
        assert response_json['name'] == search_query.name
        assert response_json['description'] == search_query.description
        assert response_json['volume'] == int(search_query.volume)
        assert response_json['measure'] == search_query.measure
        assert search_query.cost in response_json['cost']
        assert response_json['logo'] is not None

    def test_menu_filter_invalid_search(self, api_client, custom_location, custom_products_for_filtering):
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'search={custom_products_for_filtering[0].name[:2]}'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 3

class TestValidateOrderingFilter:
    def test_menu_filter_reverse_ordering(self, api_client, custom_location, custom_products_for_filtering):
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'ordering={"-volume"}'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()['results']
        assert response_json
        assert response_json[0]['cost'] > response_json[2]['cost']

    def test_menu_filter_ordering(self, api_client, custom_location, custom_products_for_filtering):
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'ordering={"volume"}'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()['results']
        assert response_json
        assert response_json[0]['volume'] < response_json[2]['volume']


class TestValidateFiltersetFilter:

    def test_menu_filterset(self, api_client, custom_location, custom_products_for_filtering):
        search_query = custom_products_for_filtering[2]
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'name={search_query.name}&cost={search_query.cost}'},
            format='json',
        )
        response_json = response.json()['results'][0]
        assert response_json
        assert response.status_code == status.HTTP_200_OK
        assert response_json['id'] == search_query.id
        assert response_json['name'] == search_query.name
        assert response_json['description'] == search_query.description
        assert response_json['volume'] == int(search_query.volume)
        assert response_json['measure'] == search_query.measure
        assert search_query.cost in response_json['cost']
        assert response_json['logo'] is not None

    def test_menu_filterset_invalid(self, api_client, custom_location, custom_products_for_filtering):
        search_query = custom_products_for_filtering[2]
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'name={search_query.name[2:]}&cost={search_query.cost[:2]}'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_200_OK
        assert response_json['results'] == []


class TestValidateRangeFilter:

    def test_menu_filter_range_one_param_to_end(self, api_client, custom_location, custom_products_for_filtering):
        """from the specified parameter to the end"""
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={range_second.cost},'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 2
        assert response.json()['results'][0]['cost'] < response.json()['results'][1]['cost']
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_beginning_to_param(self, api_client, custom_location, custom_products_for_filtering):
        """from beginning to the specified parameter"""
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost=,{range_second.cost}'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 2
        assert response.json()['results'][0]['cost'] < response.json()['results'][1]['cost']
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_param_to_param(self, api_client, custom_location, custom_products_for_filtering):
        """from the specified parameter to the specified parameter"""
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={range_first.cost},{range_second.cost}'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 2
        assert response.json()['results'][0]['cost'] < response.json()['results'][1]['cost']
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_param_to_param_reverse(self, api_client, custom_location, custom_products_for_filtering):
        """ from the specified parameter to the specified parameter
        from largest to smallest """
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={range_second.cost},{range_first.cost}'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 2
        assert response.json()['results'][0]['cost'] > response.json()['results'][1]['cost']
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_several_param(self, api_client, custom_location, custom_products_for_filtering):
        """ filter by several fields simultaneously """
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={range_second.cost},{range_first.cost}'
                               f'&range_volume={range_second.volume},{range_second.volume}'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 1
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_invalid_name_param(self, api_client, custom_location, custom_products_for_filtering):
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'rng_cost={range_second.cost},{range_first.cost}'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 3
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_invalid(self, api_client, custom_location, custom_products_for_filtering):
        """ invalid parameter - no coma after first value """
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_cost={range_second.cost}'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 3
        assert response.status_code == status.HTTP_200_OK

    def test_menu_filter_range_invalid_name(self, api_client, custom_location, custom_products_for_filtering):
        """ invalid parameter name - range_name """
        range_first, range_second, range_third = custom_products_for_filtering
        response = api_client.get(
            reverse('display_menu', args=[custom_location.code]),
            **{'QUERY_STRING': f'range_name={range_second.cost},'},
            format='json',
        )
        response_json = response.json()
        assert response_json
        assert response_json['count'] == 3
        assert response.status_code == status.HTTP_200_OK
