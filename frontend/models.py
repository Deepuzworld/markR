import uuid
from django.db import models
from django.contrib.auth.models import User

# --- Hierarchy Models ---
class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self): return self.name

class Institution(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    # This user manages the Institution (creates departments, etc.)
    admin_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='institution_admin_of')
    is_approved = models.BooleanField(default=False)
    # NEW: A flag to distinguish primary teaching institutions from others
    is_primary_academic_body = models.BooleanField(default=True)
    def __str__(self): return self.name

class Department(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration_years = models.PositiveIntegerField(default=3)
    # This user manages the department (adds students, verifies records)
    head = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_head_of')
    def __str__(self): return f"{self.name}, {self.institution.name}"

class Subject(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    semester = models.PositiveIntegerField()
    def __str__(self): return f"{self.name} (Sem {self.semester})"

# --- Student Profile ---
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    
    # --- NEW: The system-wide unique ID for sharing ---
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Fields editable by the student
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    
    def __str__(self): return self.user.username

# --- Record Models with Unified Verification ---
RECORD_TYPE_CHOICES = [
    ('UNIVERSITY', 'University Level'),
    ('COLLEGE', 'College Level'),
    ('EXTERNAL', 'External'), # New type for records added by "Other Institutions"
]

class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    # Verification can be by a Department Head (User) OR an "Other Institution".
    verified_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    verified_by_institution = models.ForeignKey(Institution, on_delete=models.PROTECT, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.student.user.username} - {self.subject.name}"

class CoCurricularRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    verified_by_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    verified_by_institution = models.ForeignKey(Institution, on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self): return f"{self.student.user.username} - {self.activity_name}"

# (ExamResult model would be updated in the same way)