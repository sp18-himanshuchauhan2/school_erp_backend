from django.contrib import admin
from .models import FeeCategory, FeeStructure, StudentFee, Payment
from schools.models import School
from classrooms.models import Classroom
from students.models import Student


@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school" and not request.user.is_superuser:
            kwargs["queryset"] = School.objects.filter(
                id=request.user.school.id)
            kwargs["initial"] = request.user.school
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'category', 'academic_year',
                    'fee_type', 'amount', 'due_date')
    list_filter = ('fee_type', 'academic_year', 'category')
    search_fields = ('classroom__class_name', 'category__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(classroom__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        school = request.user.school
        if db_field.name == 'classroom' and not request.user.is_superuser:
            kwargs['queryset'] = Classroom.objects.filter(school=school)
        elif db_field.name == 'category' and not request.user.is_superuser:
            kwargs['queryset'] = FeeCategory.objects.filter(school=school)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_structure', 'month',
                    'final_amount', 'is_paid', 'paid_date')
    list_filter = ('is_paid', 'month')
    search_fields = ('student__user__first_name',
                     'fee_structure__category__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(student__classroom__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        school = request.user.school
        if db_field.name == 'student' and not request.user.is_superuser:
            kwargs['queryset'] = Student.objects.filter(
                classroom__school=school)
        elif db_field.name == 'fee_structure' and not request.user.is_superuser:
            kwargs['queryset'] = FeeStructure.objects.filter(
                classroom__school=school)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('fee', 'amount_paid', 'payment_mode',
                    'transaction_id', 'transaction_date')
    search_fields = ('fee__student__user__first_name',
                     'payment_mode', 'transaction_id')
    list_filter = ('payment_mode', 'transaction_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(fee__student__classroom__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        school = request.user.school
        if db_field.name == 'fee' and not request.user.is_superuser:
            kwargs['queryset'] = StudentFee.objects.filter(
                student__classroom__school=school)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
