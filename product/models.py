from django.db import models
from django.utils import timezone

from Web_Menu_DA.constants import Measures


class Product(models.Model):
    company = models.ForeignKey('company.Company', related_name='product', on_delete=models.CASCADE)
    locations = models.ManyToManyField('location.Location', related_name='product_location')
    name = models.CharField('name', max_length=15)
    description = models.CharField('description', max_length=30)
    volume = models.PositiveSmallIntegerField('volume', default=0)
    # choices=list((i.value, i.name) for i in Measures) if 'class Measures(IntEnum)' in Web_Menu_DA.constant
    measure = models.PositiveSmallIntegerField('measure', choices=Measures.choices)
    cost = models.DecimalField('cost', decimal_places=2, default=0, max_digits=7)
    logo = models.OneToOneField('image.Image', related_name='product_logo', null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
