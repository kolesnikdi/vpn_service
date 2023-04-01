from django.db import models


def user_directory_path(instance, filename):    # todo It cannot be moved to another file thought a circular import
    if hasattr(instance, 'company_logo'):
        purpose = 'company_logo'
        company_id = instance.company_logo.id
    elif hasattr(instance, 'location_logo'):
        purpose = 'location_logo'
        company_id = instance.location_logo.company.id
    last_img = Image.objects.last()
    img_id = last_img.id + 1 if last_img else 1
    result = 'company_{company_id}/{purpose}/{instance_id}_{filename}'.format(
        company_id=company_id,
        purpose=purpose,
        instance_id=img_id,
        filename=filename,
    )
    return result

class Image(models.Model):
# class Image(CustomChunkIteratorModel): # Description in the custom model
    url_height = models.PositiveIntegerField(blank=True, null=True)
    url_width = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, height_field='url_height', width_field='url_width',
                              blank=True, null=True)
