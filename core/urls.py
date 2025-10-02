from django.urls import path, include
from rest_framework.routers import DefaultRouter

# --- Import ALL the NEW and correctly named ViewSets from views.py ---
# Note that 'RegisterView' has been removed and 'UniversityViewSet' has been added.
from .views import (
    UniversityViewSet,
    InstitutionViewSet,
    StudentViewSet,
    AcademicRecordViewSet,
    CoCurricularRecordViewSet,
    ExamResultViewSet
)

# Create a new router instance
router = DefaultRouter()

# --- Register all the new and updated endpoints ---
# This list now includes the 'universities' endpoint.
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'institutions', InstitutionViewSet, basename='institution')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'academic-records', AcademicRecordViewSet, basename='academicrecord')
router.register(r'cocurricular-records', CoCurricularRecordViewSet, basename='cocurricularrecord')
router.register(r'exam-results', ExamResultViewSet, basename='examresult')

# The urlpatterns list now only needs to include the router's URLs.
# The public registration URL path has been removed, as it no longer exists.
urlpatterns = [
    path('', include(router.urls)),
]