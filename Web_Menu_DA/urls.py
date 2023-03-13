from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from registration.views import WebMenuUserViewSet
from company.views import CompanyViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('company/', include('company.urls')),
    path('user/', WebMenuUserViewSet.as_view(), name='user'),
    path('company/', CompanyViewSet.as_view({'get': 'list'}), name='company'),
]
