from django.db import models
from django.utils import timezone
from django.core.validators import integer_validator

from enum import IntEnum


class Measures(IntEnum):    # or class Measures(models.IntegerChoices): # activate 21 str
    milligrams = 0
    grams = 1
    pieces = 2


class Product(models.Model):
    company = models.ForeignKey('company.Company', related_name='product', on_delete=models.CASCADE)
    locations = models.ManyToManyField('location.Location', related_name='product_location')
    name = models.CharField('name', max_length=15)
    description = models.CharField('description', max_length=30)
    volume = models.CharField('volume', validators=[integer_validator], max_length=4)
    measure = models.PositiveSmallIntegerField('measure', choices=list((i.value, i.name) for i in Measures))
    # measure = models.PositiveSmallIntegerField('measure', choices=Measures.choices) # for models.IntegerChoices
    cost = models.CharField('cost', validators=[integer_validator], max_length=4)
    logo = models.OneToOneField('image.Image', related_name='product_logo', null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
