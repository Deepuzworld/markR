from rest_framework import viewsets, permissions, status # <-- Added 'status'
from rest_framework.response import Response

# --- Import ALL the NEW Models and Serializers ---
from .models import University, Institution, Student, AcademicRecord, CoCurricularRecord, ExamResult
from .serializers import (
    UniversitySerializer, InstitutionSerializer, StudentSerializer,
    StudentProfileSerializer, AcademicRecordSerializer, CoCurricularRecordSerializer,
    ExamResultSerializer, CreateStudentSerializer
)
from .permissions import IsStudyingInstitution

# --- New and Updated ViewSets ---

class UniversityViewSet(viewsets.ModelViewSet):
    """API endpoint for Universities (managed by admin)."""
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.IsAuthenticated]

class InstitutionViewSet(viewsets.ModelViewSet):
    """API endpoint for Institutions (Colleges)."""
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- THIS IS THE FIXED CLASS ---
class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing students.
    - Institutions create students (POST).
    - Students edit their own profile (PUT/PATCH).
    """
    queryset = Student.objects.all()
    # Set the default serializer for reading data
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        # When creating a new student, use the special CreateStudentSerializer
        if self.action == 'create':
            return CreateStudentSerializer
        # When a student is updating their own profile, use the limited StudentProfileSerializer
        # We check if the user is authenticated first to avoid errors.
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Students').exists() and self.action in ['update', 'partial_update']:
            return StudentProfileSerializer
        # For all other actions (listing, retrieving), use the default StudentSerializer
        return self.serializer_class

    # --- THIS IS THE NEW METHOD THAT FIXES THE BUG ---
    def create(self, request, *args, **kwargs):
        """
        This custom create method uses the CreateStudentSerializer to validate and create,
        but then uses the StudentSerializer to show the output.
        """
        # Use the CreateStudentSerializer to process the incoming data
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        
        # This calls the .create() method in CreateStudentSerializer and gets the new Student object
        student_instance = create_serializer.save() 
        
        # Now, use the StudentSerializer to format the output correctly for the response
        read_serializer = StudentSerializer(student_instance)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # -------------------------------------------------

    def get_permissions(self):
        if self.action == 'create':
            # Only institutions can create new students.
            self.permission_classes = [IsStudyingInstitution]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated]
        else: # list, retrieve, destroy
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        # Students can only see and edit their own profile.
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='Students').exists():
            return Student.objects.filter(user=user)
        # Institutions and Admins can see all students.
        return Student.objects.all()

# --- The rest of the ViewSets remain the same ---
class AcademicRecordViewSet(viewsets.ModelViewSet):
    queryset = AcademicRecord.objects.all()
    serializer_class = AcademicRecordSerializer
    permission_classes = [IsStudyingInstitution]

    def perform_create(self, serializer):
        institution = Institution.objects.first()
        serializer.save(verified_by=institution)

class CoCurricularRecordViewSet(viewsets.ModelViewSet):
    queryset = CoCurricularRecord.objects.all()
    serializer_class = CoCurricularRecordSerializer
    permission_classes = [IsStudyingInstitution]

    def perform_create(self, serializer):
        institution = Institution.objects.first()
        serializer.save(verified_by=institution)

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = [IsStudyingInstitution]

    def perform_create(self, serializer):
        institution = Institution.objects.first()
        serializer.save(verified_by=institution)