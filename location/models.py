from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from location.business_logic import user_directory_path, validate_image_size


class Location(models.Model):
    company = models.ForeignKey('company.Company', related_name='location', on_delete=models.DO_NOTHING)
    # manager = models.ForeignKey('company.WebMenuUser', related_name='company', on_delete=models.DO_NOTHING)   # todo activate when manager will be
    url_height = models.PositiveIntegerField(blank=True, null=True)
    url_width = models.PositiveIntegerField(blank=True, null=True)
    logo = models.ImageField(upload_to=user_directory_path, height_field='url_height', width_field='url_width',
                             blank=True, null=True, validators=[validate_image_size])
    legal_name = models.CharField('legal_name', max_length=50, unique=True)
    address = models.ForeignKey('company.Address', related_name='address', on_delete=models.CASCADE)
    phone = PhoneNumberField(region='UA', max_length=13, unique=True, db_index=True,
                             error_messages={'unique': 'Not a valid mobile phone. Enter again and correctly.'})
    email = models.EmailField(verbose_name='email address', db_index=True, max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.legal_name
