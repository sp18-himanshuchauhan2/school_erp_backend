from django.contrib import admin
from .models import Exam, ExamResult, ExamSubject
from classrooms.models import Classroom
from students.models import Student
from subjects.models import Subject
from teachers.models import Teacher


class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_classrooms')

    def get_classrooms(self, obj):
        return ", ".join([str(c) for c in obj.classrooms.all()])
    get_classrooms.short_description = 'Classrooms'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(classrooms__school=request.user.school).distinct()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'classrooms':
            if request.user.is_superuser:
                kwargs["queryset"] = Classroom.objects.all()
            else:
                kwargs["queryset"] = Classroom.objects.filter(
                    school=request.user.school)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ('exam', 'classroom', 'subject', 'total_marks', 'exam_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(classroom__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'exam':
                kwargs["queryset"] = Exam.objects.filter(
                    classrooms__school=request.user.school
                ).distinct()
            elif db_field.name == 'classroom':
                kwargs["queryset"] = Classroom.objects.filter(
                    school=request.user.school)
            elif db_field.name == 'subject':
                kwargs["queryset"] = Subject.objects.filter(
                    classroomsubject__classroom__school=request.user.school
                ).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam_subject', 'student', 'marks_obtained', 'remarks')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(student__user__school=request.user.school)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'exam_subject':
                kwargs["queryset"] = ExamSubject.objects.filter(
                    classroom__school=request.user.school
                )
            elif db_field.name == 'student':
                kwargs["queryset"] = Student.objects.filter(
                    user__school=request.user.school
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamSubject, ExamSubjectAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
