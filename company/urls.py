from django.urls import path, include
from rest_framework import routers
from company.views import CreateCompanyView, CompanyViewSet

router = routers.SimpleRouter()
router.register(r'new', CreateCompanyView, basename='company_new')


urlpatterns = [
    path('', include(router.urls)),
    path('', CompanyViewSet.as_view({'get': 'list'}), name='company'),
]
