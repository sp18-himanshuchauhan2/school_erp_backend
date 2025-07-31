from django.db import models
from classrooms.models import Classroom
from students.models import Student
from schools.models import School
from django.core.exceptions import ValidationError

# Create your models here.


class FeeCategory(models.Model):
    """Types of fees: Tuition, Transport, Exam, Admission, etc."""

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('school', 'name')

    def __str__(self):
        return f"{self.name} - {self.school.name}"


class FeeStructure(models.Model):
    """Fee details mapped to a class, category, and academic year."""

    FEE_TYPE_CHOICES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
        ('one_time', 'One-time'),
    ]
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    due_date = models.DateField()

    class Meta:
        unique_together = ('classroom', 'category', 'academic_year')

    def __str__(self):
        return f"{self.classroom} | {self.category.name} | {self.academic_year}"


class StudentFee(models.Model):
    """Fee assigned to student based on structure. Tracks monthly fees too."""

    MONTH_CHOICES = [(month[:3], month) for month in [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    month = models.CharField(
        max_length=3,
        choices=MONTH_CHOICES,
        null=True,
        blank=True,
        help_text="Required for monthly fees"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'fee_structure', 'month')

    def clean(self):
        if self.fee_structure.fee_type == 'monthly' and not self.month:
            raise ValidationError("Month is required for monthly fees.")
        if self.fee_structure.fee_type != 'monthly' and self.month:
            raise ValidationError("Month should be empty for non-monthly fees.")
        
        if self.student.classroom != self.fee_structure.classroom:
            raise ValidationError(
                f"Selected student is not associated with the classroom '{self.fee_structure.classroom}' in the FeeStructure."
            )

    def __str__(self):
        return f"{self.student} - {self.fee_structure} - {self.month or 'N/A'}"


class Payment(models.Model):
    """Payment made for a particular StudentFee assignment."""

    fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.fee.student} - ₹{self.amount_paid} on {self.payment_date.date()}"
