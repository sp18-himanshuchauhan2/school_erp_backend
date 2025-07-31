from django.contrib import admin
from .models  import Student
from users.models import User
from schools.models import School
from classrooms.models import Classroom
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'classroom', 'gender', 'dob', 'enrollment_date')
    search_fields = ('user__name', 'roll_no')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs["queryset"] = User.objects.filter(role='STUDENT', school=request.user.school)
        
        elif db_field.name == 'classroom':
            if request.user.is_superuser:
                kwargs["queryset"] = Classroom.objects.all()
            else:
                kwargs["queryset"] = Classroom.objects.filter(school=request.user.school)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Student, StudentAdmin)