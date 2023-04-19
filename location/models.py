import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField


class Location(models.Model):
    company = models.ForeignKey('company.Company', related_name='location', on_delete=models.CASCADE)
    # manager = models.ForeignKey('company.WebMenuUser', related_name='company', on_delete=models.DO_NOTHING)   # todo activate when manager will be
    logo = models.OneToOneField('image.Image', related_name='location_logo', null=True, on_delete=models.CASCADE)
    legal_name = models.CharField('legal_name', max_length=50, unique=True)
    address = models.ForeignKey('address.Address', related_name='address', on_delete=models.CASCADE)
    phone = PhoneNumberField(region='UA', max_length=13, unique=True, db_index=True,
                             error_messages={'unique': 'Not a valid mobile phone. Enter again and correctly.'})
    email = models.EmailField(verbose_name='email address', db_index=True, max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    code = models.UUIDField(db_index=True, default=uuid.uuid4)


    def __str__(self):
        return self.legal_name
