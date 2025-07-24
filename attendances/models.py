from django.db import models
from students.models import Student
from classrooms.models import Classroom
from teachers.models import Teacher
from django.core.exceptions import ValidationError

# Create your models here.


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
                              ('P', 'Present'), ('A', 'Absent')])

    class Meta:
        unique_together = ('student', 'classroom', 'date')

    def __str__(self):
        return f"{self.student.user.name} - {self.status}"

    def clean(self):
        if self.classroom != self.student.classroom:
            raise ValidationError(
                "Selected student is not part of the selected classroom.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
                              ('P', 'Present'), ('A', 'Absent')])

    class Meta:
        unique_together = ('teacher', 'date')
