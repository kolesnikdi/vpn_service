import uuid
from django.db import models


class RegistrationTry(models.Model):
    email = models.EmailField(unique=True, db_index=True, max_length=254,
                              error_messages={'unique': 'Not a valid email. Enter again and correctly.'})
    code = models.UUIDField(db_index=True, default=uuid.uuid4)
    creation_time = models.DateTimeField(auto_now=True)
    confirmation_time = models.DateTimeField(null=True)
