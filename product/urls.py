from django.urls import path, include
from rest_framework import routers
from product.views import CreateProductView, ProductViewSet

router = routers.SimpleRouter()
router.register(r'new', CreateProductView, basename='product_new')


urlpatterns = [
    path('', include(router.urls)),
    path('', ProductViewSet.as_view({'get': 'list'}), name='product'),
]
