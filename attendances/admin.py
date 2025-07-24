from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance
from students.models import Student
from classrooms.models import Classroom
from teachers.models import Teacher

# Register your models here.


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'date', 'status')
    list_filter = ('date', 'status')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(student__user__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student' and not request.user.is_superuser:
            kwargs['queryset'] = Student.objects.filter(
                user__school=request.user.school)

        elif db_field.name == 'classroom' and not request.user.is_superuser:
            kwargs['queryset'] = Classroom.objects.filter(
                school=request.user.school)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'status')
    list_filter = ('date', 'status')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher__user__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher' and not request.user.is_superuser:
            kwargs['queryset'] = Teacher.objects.filter(
                user__school=request.user.school)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(TeacherAttendance, TeacherAttendanceAdmin)
