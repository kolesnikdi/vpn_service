from django.db import models
from django.core.validators import URLValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserSite(models.Model):
    owner = models.ForeignKey('registration.WebUser', related_name='user_sites', on_delete=models.CASCADE)
    site_url = models.URLField(max_length=20, unique=True, validators=[URLValidator()])
    name = models.CharField('site_name', max_length=30, unique=True)


class SiteStatistics(models.Model):
    site = models.OneToOneField('user_site.UserSite', related_name='statistics', on_delete=models.CASCADE)
    clicks_number = models.PositiveIntegerField(default=0, null=False)
    data_size = models.PositiveIntegerField(default=0, null=False)


@receiver(post_save, sender=UserSite)
def create_site_statistics(sender, instance, created, **kwargs):
    if created:
        SiteStatistics.objects.create(site=instance)
