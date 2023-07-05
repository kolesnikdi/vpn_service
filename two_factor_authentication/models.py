from django.db import models


class GoogleAuth(models.Model):
    owner = models.ForeignKey('registration.WebMenuUser', related_name='google_auth', on_delete=models.CASCADE)
    otp_base32 = models.CharField(max_length=255, null=True)
    otp_auth_url = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
