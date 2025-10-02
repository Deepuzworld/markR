from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

# Import all the models we'll need for these pages
from core.models import Student, Institution, AcademicRecord

# --- Main Navigation Views ---

def home_view(request):
    """
    Acts as the homepage, redirecting users to the login page.
    """
    return redirect('login')

def login_view(request):
    """
    Handles user login and redirects them to the correct dashboard
    based on their user group (role).
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # THIS IS THE "SMART" REDIRECT LOGIC
            if user.groups.filter(name='Studying_Institutions').exists():
                return redirect('institution_dashboard')
            elif user.groups.filter(name='Students').exists():
                return redirect('dashboard')
            else:
                # Default for other users (like superusers)
                return redirect('admin:index')
        else:
            return render(request, 'frontend/login.html', {'error': 'Invalid username or password.'})
    
    return render(request, 'frontend/login.html')

def logout_view(request):
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('login')

# --- Student-Specific Views ---

@login_required
def dashboard_view(request):
    """
    Displays the dashboard for a logged-in student.
    """
    try:
        student = Student.objects.get(user=request.user)
        context = {
            'student': student
        }
        return render(request, 'frontend/dashboard.html', context)
    except Student.DoesNotExist:
        # If a non-student user tries to access this, send them away.
        return redirect('login')

# --- NEW: Institution-Specific Views ---

@login_required
def institution_dashboard_view(request):
    """
    Displays the main dashboard for an institution, listing their students.
    """
    # In a real app, you would link a user to their specific institution.
    # For now, this placeholder gets the first institution in the database.
    try:
        institution = Institution.objects.first()
        students = Student.objects.filter(current_institution=institution)
    except Institution.DoesNotExist:
        institution = None
        students = []

    context = {
        'institution': institution,
        'students': students
    }
    return render(request, 'frontend/institution_dashboard.html', context)

@login_required
def create_student_view(request):
    """
    Handles the form for an institution to create a new student.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'frontend/create_student.html', {'error': 'A user with that username already exists.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        student_group, _ = Group.objects.get_or_create(name='Students')
        user.groups.add(student_group)

        institution = Institution.objects.first() # Placeholder
        Student.objects.create(user=user, current_institution=institution)
        
        return redirect('institution_dashboard')

    return render(request, 'frontend/create_student.html')

@login_required
def student_detail_view(request, user_id):
    """
    Shows details for a specific student and allows an institution
    to add new academic records for them.
    """
    student = Student.objects.get(user_id=user_id)
    
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        semester = request.POST.get('semester')
        grade = request.POST.get('grade')
        record_type = request.POST.get('record_type')
        
        institution = Institution.objects.first() # Placeholder for the verifier

        AcademicRecord.objects.create(
            student=student,
            course_name=course_name,
            semester=semester,
            grade=grade,
            record_type=record_type,
            verified_by=institution
        )
        return redirect('student_detail', user_id=student.user_id)

    context = {
        'student': student
    }
    return render(request, 'frontend/student_detail.html', context)