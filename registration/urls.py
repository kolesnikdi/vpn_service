from django.urls import include, path, re_path
from knox import views as knox_views

from registration import views


urlpatterns = [
    path('client_reg/', views.RegisterTryView.as_view(), name='client_reg'),
    path('owner_reg/', views.RegisterTryView.as_view(), name='owner_reg'),
    re_path(r'registration/(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/',
            views.RegisterConfirmView.as_view(), name='registration_confirm'),
    # todo Can't understand,need this string below or next 3 strings, for correct work knox token
    path('api-auth/', include('knox.urls')),
    path(r'login/', views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]
