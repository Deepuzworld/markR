from django.contrib import admin
# Import the NEW model names
from .models import University, Institution, Student, AcademicRecord, CoCurricularRecord, ExamResult

# Register the new models
admin.site.register(University)
admin.site.register(Institution)
admin.site.register(Student)
admin.site.register(AcademicRecord)
admin.site.register(CoCurricularRecord)
admin.site.register(ExamResult)