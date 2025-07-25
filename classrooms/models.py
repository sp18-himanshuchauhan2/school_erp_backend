from django.db import models
from schools.models import School
from teachers.models import Teacher

# Create your models here.


class Classroom(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='classrooms')
    class_name = models.CharField(max_length=10)
    section = models.CharField(max_length=10, blank=True, null=True)
    class_teacher = models.OneToOneField(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms_as_teacher')

    class Meta:
        unique_together = ('school', 'class_name', 'section')

    def __str__(self):
        return f"{self.class_name} - {self.section or ''} ({self.school})"
