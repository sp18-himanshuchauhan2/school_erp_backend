from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    established_year = models.PositiveIntegerField()
    # django extensions -> timestamp
    def __str__(self):
        return self.name