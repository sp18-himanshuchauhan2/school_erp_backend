from django.contrib import admin
from .models import FeeStructure, StudentFee
# Register your models here.


class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'fee_type', 'title', 'amount')
    list_filter = ('fee_type',)


class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_structure', 'month', 'is_paid', 'paid_at')
    list_filter = ('is_paid',)


admin.site.register(FeeStructure, FeeStructureAdmin)
admin.site.register(StudentFee, StudentFeeAdmin)
