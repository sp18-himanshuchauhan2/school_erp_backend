from django.contrib import admin
from .models import School

# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'contact_number', 'established_year']
    search_fields = ['name', 'contact_email']
