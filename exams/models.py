from django.db import models
from classrooms.models import Classroom
from subjects.models import Subject
from students.models import Student
from schools.models import School

# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=100)
    classrooms = models.ManyToManyField(Classroom, related_name='exams')

    class Meta:
        unique_together = ['title']

    def __str__(self):
        return self.title

class ExamSubject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="subject_schedules")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField(default=100)
    exam_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['exam', 'subject', 'classroom']

    def __str__(self):
        return f"{self.subject} - {self.exam} - {self.classroom}"

class ExamResult(models.Model):
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'exam_subject')

    def __str__(self):
        return f"{self.student} - {self.exam_subject}"
