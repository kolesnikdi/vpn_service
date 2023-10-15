from django.urls import path
from user_site.views import UserSiteView, UserSiteStatisticsView, TakeSiteAndRepresentView, vpn_service

urlpatterns = [
    path('site/new/', UserSiteView.as_view(), name='create_site'),
    path('<str:name>/', TakeSiteAndRepresentView.as_view(), name='user_site'),
    path('statistics/<str:name>/', UserSiteStatisticsView.as_view(), name='site_statistics'),
    path('<str:name>/<path:path>/', vpn_service, name='vpn_service'),
]
