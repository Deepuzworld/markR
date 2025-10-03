from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityViewSet, InstitutionViewSet, DepartmentViewSet, SubjectViewSet,
    StudentViewSet, AcademicRecordViewSet, CoCurricularRecordViewSet, ExamResultViewSet
)

router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'students', StudentViewSet)
router.register(r'academic-records', AcademicRecordViewSet)
router.register(r'cocurricular-records', CoCurricularRecordViewSet)
router.register(r'exam-results', ExamResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]