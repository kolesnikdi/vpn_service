from django.urls import path, re_path

from registration import views


urlpatterns = [
    path('', views.RegisterTryView.as_view(), name='user_reg'),
    re_path(r'(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/',
            views.RegisterConfirmView.as_view(), name='registration_confirm'),
]
