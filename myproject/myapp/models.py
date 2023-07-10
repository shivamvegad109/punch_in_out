from django.db import models
from django.utils import timezone
import uuid
from datetime import datetime


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    punchin_time = models.DateTimeField(null=True, blank=True)
    punchout_time = models.DateTimeField(null=True, blank=True)
    is_in = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)
    working = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email