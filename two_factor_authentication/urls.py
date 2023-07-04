from django.urls import path
from two_factor_authentication.views import Enable2FAView, DisplayQrView

urlpatterns = [
    path('', Enable2FAView.as_view(), name='enable2fa'),
    path('display_qr', DisplayQrView.as_view(), name='display_qr'),
]
