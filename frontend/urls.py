
from django.urls import path
from .views import (
    home_view,
    login_view,
    logout_view,
    institution_register_view,
    registration_pending_view,
    institution_dashboard_view,
    create_department_view,
    assign_head_view,
)

urlpatterns = [
    # General pages
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # --- NEW INSTITUTION REGISTRATION ---
    path('register/institution/', institution_register_view, name='institution_register'),
    path('register/pending/', registration_pending_view, name='registration_pending'),

    path('institution/dashboard/', institution_dashboard_view, name='institution_dashboard'),
    path('institution/department/create/', create_department_view, name='create_department'),
    # This URL will be for a page to assign a head to a specific department
    path('institution/department/<int:dept_id>/assign-head/', assign_head_view, name='assign_head'),

]