from django.urls import reverse
from user_site.models import UserSite


class TestView:

    def test_for_debug_first_enter(self, authenticated_client):
        site = UserSite.objects.create(owner=authenticated_client.user, site_url='https://espreso.tv/', name='espreso')
        url = reverse('user_site', args=[site.name])
        response = authenticated_client.get(url, format='json')
        assert response.status_code == 200

    def test_for_debug_vpn_service(self, authenticated_client):
        site = UserSite.objects.create(owner=authenticated_client.user, site_url='https://espreso.tv/', name='espreso')
        url = reverse('vpn_service', args=[site.name, 'espreso.tv/news/'])
        response = authenticated_client.get(url, format='json')
        assert response.status_code == 200

