from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class School(TimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    established_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name