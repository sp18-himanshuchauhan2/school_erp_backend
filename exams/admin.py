from django.contrib import admin
from .models import Exam, ExamResult, ExamSubject
from classrooms.models import Classroom
# Register your models here.


class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'classroom':
            if request.user.is_superuser:
                kwargs["queryset"] = Classroom.objects.all()
            else:
                kwargs["queryset"] = Classroom.objects.filter(
                    school=request.user.school)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ('exam', 'subject', 'total_marks')


class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam_subject', 'student', 'marks_obtained', 'remarks')


admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamSubject, ExamSubjectAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
