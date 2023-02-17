from django.urls import include, path, re_path
from rest_framework import routers
from knox import views as knox_views

from registration.views import RegisterTryView, RegisterConfirmView, LoginView, WebMenuUserViewSet

# router = routers.DefaultRouter()
# router.register(r'user', WebMenuUserViewSet)

urlpatterns = [
    path('', RegisterTryView.as_view(), name='user_reg'),
    re_path(r'(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/',
            RegisterConfirmView.as_view(), name='registration_confirm'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('user/', WebMenuUserViewSet.as_view()),
    # path('', include(router.urls)),
]
