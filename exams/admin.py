from django.contrib import admin
from .models import Exam, ExamResult, ExamSubject
from classrooms.models import Classroom
# Register your models here.


class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_classrooms')

    def get_classrooms(self, obj):
        return ", ".join([str(c) for c in obj.classrooms.all()])
    get_classrooms.short_description = 'Classrooms'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'classrooms':
            if request.user.is_superuser:
                kwargs["queryset"] = Classroom.objects.all()
            else:
                kwargs["queryset"] = Classroom.objects.filter(
                    school=request.user.school)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ('exam', 'classroom', 'subject', 'total_marks')


class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam_subject', 'student', 'marks_obtained', 'remarks')


admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamSubject, ExamSubjectAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
