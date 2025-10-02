from django.urls import path

# Import all the views from our views.py file
from .views import (
    home_view,
    login_view,
    logout_view,
    dashboard_view,
    institution_dashboard_view,
    create_student_view,
    student_detail_view,
)

urlpatterns = [
    # General pages
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Student-specific pages
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Institution-specific pages
    path('institution/dashboard/', institution_dashboard_view, name='institution_dashboard'),
    path('institution/student/create/', create_student_view, name='create_student'),
    # This URL pattern captures the student's ID from the URL, e.g., /institution/student/3/
    path('institution/student/<int:user_id>/', student_detail_view, name='student_detail'),
]