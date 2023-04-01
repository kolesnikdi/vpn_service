from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, integer_validator

from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    owner = models.ForeignKey('registration.WebMenuUser', related_name='company', on_delete=models.DO_NOTHING)
    logo = models.OneToOneField('image.Image', related_name='company_logo', null=True, on_delete=models.CASCADE)
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
