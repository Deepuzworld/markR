# This file will contain all the "translators" for our models.

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import (
    University, Institution, Department, Subject, Student,
    AcademicRecord, CoCurricularRecord, ExamResult
)

# --- Hierarchy Serializers ---
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

# --- User/Student Creation and Management Serializers ---
class CreateStudentSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    department_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        student_group, _ = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)
        department = Department.objects.get(id=validated_data['department_id'])
        student = Student.objects.create(user=user, department=department)
        return student

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['photo', 'phone_no', 'contact_email']

# --- Record Serializers ---
class AcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = '__all__'

class CoCurricularRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoCurricularRecord
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'

# --- Main Student Detail Serializer (for Reading) ---
class StudentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    academic_records = AcademicRecordSerializer(many=True, read_only=True, source='academicrecord_set')
    cocurricular_records = CoCurricularRecordSerializer(many=True, read_only=True, source='cocurricularrecord_set')
    exam_results = ExamResultSerializer(many=True, read_only=True, source='examresult_set')
    
    class Meta:
        model = Student
        fields = [
            'user', 'public_id', 'department', 'photo', 'phone_no', 'contact_email',
            'academic_records', 'cocurricular_records', 'exam_results'
        ]