from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('company', '0005_alter_company_actual_address_and_more'),
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""
                INSERT INTO image_image (
                    url_height,
                    url_width,
                    image,
                    company_id
                )
                SELECT 
                    url_height,
                    url_width,
                    logo,
                    id
                FROM
                    company_company;
            """),
    ]
