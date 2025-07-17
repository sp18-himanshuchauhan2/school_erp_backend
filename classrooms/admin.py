from django.contrib import admin
from .models import Classroom
from schools.models import School

# Register your models here.

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['school', 'class_name', 'section']
    search_fields = ['class_name', 'section']

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(school=request.user.school)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'school' and not request.user.is_superuser:
            kwargs['queryset'] = School.objects.filter(id=request.user.school.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(Classroom, ClassroomAdmin)