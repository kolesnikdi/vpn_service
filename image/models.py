from django.db import models

from image.business_logic import user_directory_path


class Image(models.Model):
# class Image(CustomChunkIteratorModel): # Description in the custom model
    url_height = models.PositiveIntegerField(blank=True, null=True)
    url_width = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, height_field='url_height', width_field='url_width',
                              blank=True, null=True)
