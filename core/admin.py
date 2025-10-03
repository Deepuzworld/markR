from django.contrib import admin
from .models import (
    University, Institution, Department, Subject,
    Student, AcademicRecord, CoCurricularRecord, ExamResult
)

# --- NEW: A custom admin class for Institutions ---
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    # This controls which fields are displayed in the list view
    list_display = ('name', 'university', 'admin_user', 'is_approved', 'is_primary_academic_body')
    
    # This adds a filter sidebar
    list_filter = ('is_approved', 'university')
    
    # This makes the 'name' field a clickable link to the detail view
    list_display_links = ('name',)
    
    # This adds a search bar
    search_fields = ('name', 'admin_user__username')
    
    # --- THIS IS THE APPROVAL ACTION ---
    actions = ['approve_institutions']

    @admin.action(description='Approve selected institutions')
    def approve_institutions(self, request, queryset):
        """
        This action updates the selected institutions' 'is_approved' status to True.
        """
        queryset.update(is_approved=True)
        self.message_user(request, f"Successfully approved {queryset.count()} institution(s).")

# --- Register the other models in the simple way ---
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(AcademicRecord)
admin.site.register(CoCurricularRecord)
admin.site.register(ExamResult)