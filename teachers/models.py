from django.db import models
from config import settings
from schools.models import School

# Create your models here.
class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text='Experience in years')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    subject_spec = models.CharField(max_length=100, verbose_name='Subject_Specialization')
    dob = models.DateField(verbose_name='Date of Birth')
    join_date = models.DateField()

    def __str__(self):
        return f"{self.user.name} ({self.subject_spec})"