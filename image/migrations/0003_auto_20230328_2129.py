from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_auto_20230328_2049'),
    ]

    operations = [
            migrations.RunSQL("""
                    INSERT INTO image_image (
                        url_height,
                        url_width,
                        image,
                        location_id
                    )
                    SELECT 
                        url_height,
                        url_width,
                        logo,
                        id
                    FROM
                        location_location;
                """)
        ]
