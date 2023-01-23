from django.urls import include, path, re_path
from rest_framework import routers

from registration import views

from knox import views as knox_views
from registration.views import LoginView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('registration/', views.RegisterTryView.as_view(), name='registration'),
    re_path(r'registration/(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/',
            views.RegisterConfirmView.as_view(), name='registration_confirm'),
    # """Can't understand,need this string below or next 3 strings, for correct work knox token"""
    path('api-auth/', include('knox.urls', namespace='knox')),
    path(r'login/', LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

    path('', include(router.urls)),
]
