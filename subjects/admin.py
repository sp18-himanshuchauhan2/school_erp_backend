from django.contrib import admin
from .models import Subject, ClassroomSubject
from schools.models import School
from classrooms.models import Classroom
from teachers.models import Teacher

# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['school', 'name']
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(school=request.user.school)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'school' and not request.user.is_superuser:
            kwargs['queryset'] = School.objects.filter(id=request.user.school.id)
            kwargs['initial'] = request.user.school
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ClassroomSubjectAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'subject', 'teacher']
    search_fields = ['subject_name', 'classroom__class_name', 'teacher__user__first_name']
    list_filter = ['classroom__class_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(classroom__school=request.user.school)

    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            try:
                school = School.objects.get(user=request.user)
                form.base_fields['classroom'].queryset = Classroom.objects.filter(school=school)
                form.base_fields['subject'].queryset = Subject.objects.filter(school=school)
                form.base_fields['teacher'].queryset = Teacher.objects.filter(user__school=school)
            except School.DoesNotExist:
                form.base_fields['classroom'].queryset = Classroom.objects.none()
                form.base_fields['subject'].queryset = Subject.objects.none()
                form.base_fields['teacher'].queryset = Teacher.objects.none()
        return form

admin.site.register(Subject, SubjectAdmin)
admin.site.register(ClassroomSubject, ClassroomSubjectAdmin)
