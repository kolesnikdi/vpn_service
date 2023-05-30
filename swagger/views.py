from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

DESCRIPTION = """ 
Project `Web_Menu_DA`. 
"""

SchemaView = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
        description=DESCRIPTION,
        contact=openapi.Contact(email='segareta@ukr.net'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
