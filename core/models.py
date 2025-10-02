from django.db import models
from django.contrib.auth.models import User

# ==============================================================================
# NEW MODEL: The top of the hierarchy, managed by the Admin.
# ==============================================================================
class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name

# ==============================================================================
# MODIFIED MODEL: Now linked to a University.
# ==============================================================================
class Institution(models.Model):
    # This is now a "College" in the hierarchy
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return f"{self.name} ({self.university.name})"

# ==============================================================================
# MODIFIED MODEL: Added fields for students to edit themselves.
# ==============================================================================
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # The institution that currently holds the student's records
    current_institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- NEW: Fields editable by the student ---
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    # The user's primary email will be on the User model, this can be a secondary one
    contact_email = models.EmailField(null=True, blank=True)

    # Note: Students cannot be removed, so we don't need a status field.
    # To "deactivate", an admin could deactivate their User account.

    def __str__(self):
        return self.user.username

# ==============================================================================
# MODIFIED MODELS: Added verification and record types.
# ==============================================================================
RECORD_TYPE_CHOICES = [
    ('UNIVERSITY', 'University Level'),
    ('COLLEGE', 'College Level'),
]

class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    semester = models.PositiveIntegerField()
    grade = models.CharField(max_length=5)
    
    # --- NEW: Verification Fields ---
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    verified_by = models.ForeignKey(Institution, on_delete=models.PROTECT, help_text="The institution that verified this record.")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course_name}"

class CoCurricularRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

    # --- NEW: Verification Fields ---
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    verified_by = models.ForeignKey(Institution, on_delete=models.PROTECT, help_text="The institution that verified this record.")

    def __str__(self):
        return f"{self.student.user.username} - {self.activity_name}"
    


class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    score = models.FloatField()
    
    # --- NEW: Verification Fields ---
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    verified_by = models.ForeignKey(Institution, on_delete=models.PROTECT, help_text="The institution that verified this record.")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.exam_name}"    