from django.db import models
from classrooms.models import Classroom
from students.models import Student

# Create your models here.


class FeeStructure(models.Model):
    FEE_TYPE_CHOICES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
        ('one_time', 'OneTime'),
    ]
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    fee_type = models.CharField(
        max_length=20, choices=FEE_TYPE_CHOICES, default='monthly')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('classroom', 'amount')

    def __str__(self):
        return f"{self.title}-{self.amount}"


class StudentFee(models.Model):
    MONTH_CHOICES = [
        ('Jan', 'January'),
        ('Feb', 'February'),
        ('Mar', 'March'),
        ('Apr', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('Aug', 'August'),
        ('Sept', 'September'),
        ('Oct', 'October'),
        ('Nov', 'November'),
        ('Dec', 'December'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'fee_structure', 'month')
