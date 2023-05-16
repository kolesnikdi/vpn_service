from django.urls import path, include
from rest_framework import routers
from company.views import CreateCompanyView, CompanyViewSet

router = routers.SimpleRouter()
router.register(r'new', CreateCompanyView, basename='company_new')


urlpatterns = [
    path('', include(router.urls)),
    path('', CompanyViewSet.as_view({'get': 'list'}), name='company'),
]

# urlpatterns = [
#     path('', CompanyView.as_view(), name='companyRC'),  # post -> create one, get -> list of
#     path(r'{company_id}', CompanyViewRUD.as_view(), name='companyRUD'),  # get -> get company_id,, update -> update company_id, delete -> delete company_id,
# ]
