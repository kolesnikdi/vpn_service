from django.urls import path, re_path
from knox.views import LogoutView, LogoutAllView

from registration.views import RegisterTryView, RegisterConfirmView, LoginView, WebMenuUserViewSet


urlpatterns = [
    path('', RegisterTryView.as_view(), name='user_reg'),
    re_path(r'(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/',
            RegisterConfirmView.as_view(), name='registration_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logoutall/', LogoutAllView.as_view(), name='logoutall'),
    path('user/', WebMenuUserViewSet.as_view(), name='user'),
]
