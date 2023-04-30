from django.urls import re_path

from menu.views import ProductMenuView, LocationMenuView

urlpatterns = [
    re_path(r'^(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',
            ProductMenuView.as_view({'get': 'list'}), name='display_menu'),
    re_path(r'^list/(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',
            LocationMenuView.as_view(), name='list_menu'),
]
