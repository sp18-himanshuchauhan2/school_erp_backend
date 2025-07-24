from django.db import models
from classrooms.models import Classroom
from users.models import User

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    roll_no = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[
                              ('M', 'Male'), ('F', 'Female')])
    dob = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['classroom', 'roll_no']

    def __str__(self):
        return f"{self.user.name} ({self.user.school})"
