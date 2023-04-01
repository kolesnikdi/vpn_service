from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
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
