from rest_framework import serializers
from django.contrib.auth.models import User, Group
# Import ALL the new models, including University and ExamResult
from .models import University, Institution, Student, AcademicRecord, CoCurricularRecord, ExamResult

# --- Serializers for University and Institution ---
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

# --- Serializers for Creating and Managing Students ---
class CreateStudentSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    def create(self, validated_data):
        # This logic handles creating the User and the linked Student profile
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        student_group, _ = Group.objects.get_or_create(name='Students')
        user.groups.add(student_group)
        
        # In a real app, you would get this from the logged-in institution user's profile
        current_institution = Institution.objects.first()
        student = Student.objects.create(user=user, current_institution=current_institution)
        return student

class StudentProfileSerializer(serializers.ModelSerializer):
    # This is for students to edit their own limited set of fields
    class Meta:
        model = Student
        fields = ['photo', 'phone_no', 'contact_email']

# --- Serializers for Records (including ExamResult) ---
class AcademicRecordSerializer(serializers.ModelSerializer):
    verified_by = serializers.StringRelatedField()
    class Meta:
        model = AcademicRecord
        fields = '__all__'

class CoCurricularRecordSerializer(serializers.ModelSerializer):
    verified_by = serializers.StringRelatedField()
    class Meta:
        model = CoCurricularRecord
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer): # <-- ADDED BACK IN
    verified_by = serializers.StringRelatedField()
    class Meta:
        model = ExamResult # <-- Uses the correct, updated ExamResult model
        fields = '__all__'

# --- Main Serializer for Viewing a Student's Full Profile ---
class StudentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    current_institution = serializers.StringRelatedField()
    
    # Add all the record types to the nested view
    academic_records = AcademicRecordSerializer(many=True, read_only=True, source='academicrecord_set')
    cocurricular_records = CoCurricularRecordSerializer(many=True, read_only=True, source='cocurricularrecord_set')
    exam_results = ExamResultSerializer(many=True, read_only=True, source='examresult_set') # <-- ADDED BACK IN

    class Meta:
        model = Student
        fields = [
            'user', 'current_institution', 'photo', 'phone_no', 'contact_email',
            'academic_records', 'cocurricular_records', 'exam_results' # <-- ADDED BACK IN
        ]
        