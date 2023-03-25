from django.urls import path, include
from rest_framework import routers
from location.views import CreateLocationView, LocationViewSet

router = routers.SimpleRouter()
router.register(r'new', CreateLocationView, basename='location_new')


urlpatterns = [
    path('', include(router.urls)),
    path('', LocationViewSet.as_view({'get': 'list'}), name='location'),
]
