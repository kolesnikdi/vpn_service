from django.contrib import admin
from django.urls import include, path

from registration.views import WebMenuUserViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('company/', include('company.urls')),
    path('location/', include('location.urls')),
    path('product/', include('product.urls')),
    path('user/', WebMenuUserViewSet.as_view(), name='user'),
]
