from django.db import migrations

from Web_Menu_DA.custom_utils import custom_queryset_iterator
from company.models import Company
from image.models import Image
from location.models import Location


def copy_images_ids(apps, schema):
    CHUNK_SIZE = 3

    company_images = Image.objects.filter(company_id__isnull=False).select_related('company')

    for img_qs in custom_queryset_iterator(company_images, CHUNK_SIZE):
        companies_to_update = []
        for img in img_qs:
            img.company.logo_id = img.id
            companies_to_update.append(img.company)
        Company.objects.bulk_update(companies_to_update, ['logo_id'])

    location_images = Image.objects.filter(location_id__isnull=False).select_related('location')

    for img_qs in custom_queryset_iterator(location_images, CHUNK_SIZE):
        locations_to_update = []
        for img in img_qs:
            img.location.logo_id = img.id
            locations_to_update.append(img.location)
        Location.objects.bulk_update(locations_to_update, ['logo_id'])


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('image', '0003_auto_20230328_2129'),
        ('location', '0007_location_logo'),
        ('company', '0007_company_logo'),
    ]

    operations = [
        migrations.RunPython(code=copy_images_ids)
    ]
