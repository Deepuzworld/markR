from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import (
    University, Institution, Department, Subject, Student,
    AcademicRecord, CoCurricularRecord, ExamResult
)
from .serializers import (
    UniversitySerializer, InstitutionSerializer, DepartmentSerializer, SubjectSerializer,
    StudentSerializer, StudentProfileSerializer, CreateStudentSerializer,
    AcademicRecordSerializer, CoCurricularRecordSerializer, ExamResultSerializer
)
from .permissions import IsInstitutionAdmin, IsDepartmentHead, IsStudent

# --- ViewSets for Hierarchy (Mostly for Admins) ---
class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.IsAdminUser] # Only superusers can manage universities

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated] # Read-only for most, admin for write

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsInstitutionAdmin] # Only Institution Admins can manage depts

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsDepartmentHead] # Only Dept Heads can manage subjects

# --- Main Student ViewSet ---
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        if self.action == 'create': return CreateStudentSerializer
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Student').exists() and self.action in ['update', 'partial_update']:
            return StudentProfileSerializer
        return StudentSerializer

    def get_permissions(self):
        if self.action == 'create': self.permission_classes = [IsDepartmentHead]
        elif self.action in ['update', 'partial_update']: self.permission_classes = [permissions.IsAuthenticated]
        else: self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated: return Student.objects.none()
        if user.groups.filter(name='Student').exists():
            return Student.objects.filter(user=user)
        # Add logic here for Dept Heads to see only their students
        return Student.objects.all()

# --- Record ViewSets (Managed by Dept Heads) ---
class AcademicRecordViewSet(viewsets.ModelViewSet):
    queryset = AcademicRecord.objects.all()
    serializer_class = AcademicRecordSerializer
    permission_classes = [IsDepartmentHead]

    def perform_create(self, serializer):
        serializer.save(verified_by_user=self.request.user, record_type='COLLEGE')

class CoCurricularRecordViewSet(viewsets.ModelViewSet):
    queryset = CoCurricularRecord.objects.all()
    serializer_class = CoCurricularRecordSerializer
    permission_classes = [IsDepartmentHead]

    def perform_create(self, serializer):
        serializer.save(verified_by_user=self.request.user, record_type='COLLEGE')

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = [IsDepartmentHead]

    def perform_create(self, serializer):
        serializer.save(verified_by_user=self.request.user, record_type='COLLEGE')