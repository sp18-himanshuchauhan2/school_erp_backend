from django.contrib import admin, messages
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from schools.models import School
from django.core.exceptions import ValidationError

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'role', 'school', 'is_staff', 'is_superuser']
    list_filter = ['role', 'school']
    ordering = ['email']
    search_fields = ['email']
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'address')}),
        ('School Info', {'fields': ('role', 'school')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'school', 'phone', 'address', 'password1', 'password2', 'user_permissions'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'SCHOOL_ADMIN' and not request.user.is_superuser:
            return qs.filter(school=request.user.school)
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'school' and request.user.role == 'SCHOOL_ADMIN' and not request.user.is_superuser:
            kwargs['queryset'] = School.objects.filter(id=request.user.school.id)
            kwargs['initial'] = request.user.school
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'role' and request.user.role == 'SCHOOL_ADMIN' and not request.user.is_superuser:
            allowed_roles = ['SCHOOL_ADMIN', 'TEACHER', 'STUDENT']
            kwargs['choices'] = [
                (key, label) for key, label in db_field.choices if key in allowed_roles
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def changelist_view(self, request, extra_context = None):
        if request.user.role == 'SCHOOL_ADMIN':
            messages.info(request, f"You are School Admin of {request.user.school.name}")
        return super().changelist_view(request, extra_context=extra_context)
    
    def save_model(self, request, obj, form, change):
        if request.user.role == 'SCHOOL_ADMIN' and not request.user.is_superuser:
            obj.school = request.user.school

            if obj.role not in ['SCHOOL_ADMIN', 'TEACHER', 'STUDENT']:
                raise ValidationError("You do not have permission to assign this role.")
            
        if request.user.role == 'MAIN_ADMIN' and obj.role == 'SCHOOL_ADMIN':
            obj.is_staff = True

        return super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)