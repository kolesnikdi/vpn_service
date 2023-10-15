from rest_framework import serializers
from user_site.models import UserSite, SiteStatistics


class UserSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSite
        fields = ['site_url', 'name']


class UserSiteStatisticsSerializer(serializers.ModelSerializer):

    site_url = serializers.CharField(source='site.site_url')

    class Meta:
        model = SiteStatistics
        fields = ['site_url', 'clicks_number', 'data_size']

