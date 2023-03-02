import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy
from registration.managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField


class RegistrationTry(models.Model):
    email = models.EmailField(unique=True, db_index=True, max_length=254,
                              error_messages={'unique': 'Not a valid email. Enter again and correctly.'})
    code = models.UUIDField(db_index=True, default=uuid.uuid4)
    creation_time = models.DateTimeField(auto_now=True)
    confirmation_time = models.DateTimeField(null=True)

class WebMenuUser(AbstractBaseUser, PermissionsMixin):

    username = None
    mobile_phone = PhoneNumberField(region='UA', max_length=13, unique=True, db_index=True,
                                    error_messages={'unique': 'Not a valid mobile phone. Enter again and correctly.'})
    first_name = models.CharField('first name', max_length=30, null=True)
    last_name = models.CharField('last name', max_length=30, null=True)
    fathers_name = models.CharField('fathers name', max_length=20)
    country = models.CharField('country', max_length=30)
    city = models.CharField('city', max_length=30)
    street = models.CharField('street', max_length=50)
    house_number = models.CharField('house number', max_length=10)
    flat_number = models.CharField('flat number', max_length=10)
    passport_series = models.CharField('passport series', max_length=2)
    passport_number = models.CharField('passport number', max_length=6)
    passport_date_of_issue = models.DateField('passport date of issue', null=True)
    passport_issuing_authority = models.CharField('passport issuing authority', max_length=100)
    email = models.EmailField(gettext_lazy('email address'), unique=True, db_index=True, max_length=254,
                              error_messages={'unique': 'Not a valid email. Enter again and correctly.'})
    password = models.CharField('password', max_length=128)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()   # """ Need to createsuperuser"""

    def __str__(self):
        return self.email

