from django.db import models


class Address(models.Model):
    country = models.CharField('legal country', max_length=30)
    city = models.CharField('legal city', max_length=30)
    street = models.CharField('legal street', max_length=50)
    house_number = models.CharField('legal house number', max_length=10)
    flat_number = models.CharField('legal flat number', max_length=10)