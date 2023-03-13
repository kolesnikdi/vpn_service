from django.urls import path, include
from rest_framework import routers
from company.views import CreateCompanyView

router = routers.SimpleRouter()
router.register(r'new', CreateCompanyView, basename='company_new')


urlpatterns = [
    path('', include(router.urls)),
]
