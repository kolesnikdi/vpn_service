from django.urls import include, path
from rest_framework import routers

from client.views import ClientViewSet

router = routers.DefaultRouter()
router.register(r'client', ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
