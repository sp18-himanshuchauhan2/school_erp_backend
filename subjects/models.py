from django.db import models
from classrooms.models import Classroom
from teachers.models import Teacher
from schools.models import School

# Create your models here.

class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name
    
class ClassroomSubject(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('classroom', 'subject')

    def __str__(self):
        return f'{self.subject.name} -> {self.classroom.class_name} {self.classroom.section}'