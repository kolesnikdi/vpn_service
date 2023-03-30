from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, integer_validator

from phonenumber_field.modelfields import PhoneNumberField
from company.business_logic import user_directory_path, validate_image_size

# class Logo(models.Model): # todo make separate application for Image
# logo = models.ForeignKey(Logo, null=True, on_delete=models.CASCADE)   # todo move request to Company


class Company(models.Model):
    owner = models.ForeignKey('registration.WebMenuUser', related_name='company', on_delete=models.DO_NOTHING)
    url_height = models.PositiveIntegerField(blank=True, null=True)
    url_width = models.PositiveIntegerField(blank=True, null=True)
    logo = models.ImageField(upload_to=user_directory_path, height_field='url_height', width_field='url_width',
                             blank=True, null=True, validators=[validate_image_size])
    legal_name = models.CharField('legal_name', max_length=50, unique=True)
    legal_address = models.ForeignKey('address.Address', related_name='legal_address', on_delete=models.CASCADE)
    actual_address = models.ForeignKey('address.Address', related_name='actual_address', on_delete=models.CASCADE)
    code_USREOU = models.CharField('code USREOU', validators=[MinLengthValidator(8), integer_validator], max_length=10
                                   , unique=True)
    phone = PhoneNumberField(region='UA', max_length=13, unique=True, db_index=True,
                             error_messages={'unique': 'Not a valid mobile phone. Enter again and correctly.'})
    email = models.EmailField(verbose_name='email address', unique=True, db_index=True, max_length=50,
                              error_messages={'unique': 'Not a valid email. Enter again and correctly.'})
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.legal_name
