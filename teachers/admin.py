from django.contrib import admin
from .models import Teacher
from schools.models import School
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject_spec', 'qualification',
                    'experience', 'gender', 'dob', 'join_date', ]
    search_fields = ['user__name', 'subject_spec']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            school = School.objects.get(user=request.user)
            return qs.filter(user__school=school)
        except School.DoesNotExist:
            return Teacher.objects.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            if request.user.is_superuser:
                kwargs['queryset'] = User.objects.filter(role='TEACHER')
            else:
                school = getattr(request.user, 'school', None)
                if school:
                    kwargs['queryset'] = User.objects.filter(
                        role='TEACHER', school=school)
                else:
                    kwargs['queryset'] = User.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Teacher, TeacherAdmin)
