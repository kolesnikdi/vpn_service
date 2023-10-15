from requests import get
from bs4 import BeautifulSoup

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from user_site.business_logic import remake_links, count_site_data, get_method, authenticate_and_get_site
from user_site.models import UserSite
from user_site.serializers import UserSiteSerializer, UserSiteStatisticsSerializer
from vpn_service.permissions import IsOwnerOr404
from urllib.parse import urlparse


class UserSiteView(generics.CreateAPIView):
    """To create Site."""
    queryset = UserSite.objects.all()
    serializer_class = UserSiteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserSite.objects.create(owner=request.user, **serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TakeSiteAndRepresentView(generics.RetrieveAPIView):
    """Uses only 'GET' method. For the first access to the site."""
    queryset = UserSite.objects.all()
    serializer_class = UserSiteStatisticsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOr404]

    def get(self, request, *args, **kwargs):
        site = generics.get_object_or_404(self.queryset, name=kwargs['name'])
        content = get(site.site_url).content
        count_site_data(site, request, content)
        soup = BeautifulSoup(content, 'html.parser')
        soup = remake_links(soup, site)
        return HttpResponse(str(soup))


def vpn_service(request, name, path, **kwargs):
    """Uses all methods. For moving across the entire site"""
    site = authenticate_and_get_site(request, name)
    parsed_url = urlparse(site.site_url)
    original_url = f'{parsed_url.scheme}://{path}'
    if not(method := get_method(request)):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    content = method(original_url, **kwargs).content
    count_site_data(site, request, content)
    soup = BeautifulSoup(content, 'html.parser')
    soup = remake_links(soup, site)
    return HttpResponse(str(soup))


class UserSiteStatisticsView(generics.RetrieveAPIView):
    """To view site statistics"""
    queryset = UserSite.objects.all()
    serializer_class = UserSiteStatisticsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOr404]

    def get_object(self):
        site = self.get_queryset().get(name=self.kwargs['name'])
        return site.statistics
