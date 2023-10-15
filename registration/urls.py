from django.urls import path
from knox.views import LogoutView, LogoutAllView

from registration.views import RegisterConfirmView, LoginView, WebUserUpdateView, WebUserViewSet

urlpatterns = [
    path('registration/', RegisterConfirmView.as_view(), name='registration'),
    path('user/', WebUserViewSet.as_view(), name='user'),
    path('user/<int:id>/', WebUserUpdateView.as_view(), name='update_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logoutall/', LogoutAllView.as_view(), name='logoutall'),
]
