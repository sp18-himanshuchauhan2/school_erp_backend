from django.contrib import admin
from .models import School

# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact_email', 'contact_number', 'established_year']
    search_fields = ['name', 'contact_email']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, "role") and request.user.role == "SCHOOL_ADMIN":
            return qs.filter(id=request.user.school_id)
        return qs.none()
