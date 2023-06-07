from django.urls import path, re_path
from knox.views import LogoutView, LogoutAllView

from registration.djng_views import DjangoRegisterTryView, django_register_try_function, \
    django_register_confirm_function
from registration.views import RegisterTryView, RegisterConfirmView, LoginView


urlpatterns = [
    path('', RegisterTryView.as_view(), name='user_reg'),
    # Always open regex with ^ and close with $. This will prevent another regex from overlapping
    re_path(r'^(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',
            RegisterConfirmView.as_view(),
            name='registration_confirm',
            ),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logoutall/', LogoutAllView.as_view(), name='logoutall'),

    # django generic edit class CreateView
    path('djangoform/', DjangoRegisterTryView.as_view(), name='djangoform'),

    # function based view
    path('djangofunction/', django_register_try_function, name='djangofunction'),
    re_path(r'^djangofunction/(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',
            django_register_confirm_function,
            name='djangofunction_confirm',
            ),
]
