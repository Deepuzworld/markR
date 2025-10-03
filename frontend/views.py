from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # Added for new views
from core.models import University, Institution, Department # Added Department to imports

# --- CORE FRONTEND VIEWS ---

def home_view(request):
    """Redirects the homepage to the login page."""
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # --- UPDATED LOGIC for Rerouting based on Role ---
            if user.groups.filter(name='Institution_Admin').exists():
                return redirect('institution_dashboard')
            
            # Now we can add the Department Head logic
            elif user.groups.filter(name='Department_Head').exists():
                return redirect('department_dashboard') # Assuming you will create this later

            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
                
            elif user.is_superuser:
                return redirect('admin:index')
                
            # Fallback for users who are logged in but don't match a specific group
            return redirect('home') 
        else:
            # Handle invalid login
            return render(request, 'frontend/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'frontend/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- NEW REGISTRATION VIEWS ---

def institution_register_view(request):
    """Handles the registration form for new institutions."""
    universities = University.objects.all()
    if not universities.exists():
        return render(request, 'frontend/error.html', {'message': 'No Universities are available in the system. Please contact the administrator.'})

    if request.method == 'POST':
        institution_name = request.POST.get('institution_name')
        university_id = request.POST.get('university')
        admin_username = request.POST.get('admin_username')
        admin_email = request.POST.get('admin_email')
        admin_password = request.POST.get('admin_password')

        if User.objects.filter(username=admin_username).exists():
            return render(request, 'frontend/institution_register.html', {
                'error': 'An admin with this username already exists.',
                'universities': universities
            })
        
        admin_user = User.objects.create_user(
            username=admin_username, email=admin_email, password=admin_password
        )
        inst_admin_group, _ = Group.objects.get_or_create(name='Institution_Admin')
        admin_user.groups.add(inst_admin_group)

        university = University.objects.get(id=university_id)
        Institution.objects.create(
            name=institution_name,
            university=university,
            admin_user=admin_user,
            is_approved=False # Registrations are NOT approved by default
        )
        
        return redirect('registration_pending')

    return render(request, 'frontend/institution_register.html', {'universities': universities})


def registration_pending_view(request):
    """A simple page to inform the user their registration is pending approval."""
    return render(request, 'frontend/registration_pending.html')

# ----------------------------------------------------------------------------------
# --- INSTITUTION ADMIN VIEWS (New additions) ---
# ----------------------------------------------------------------------------------

@login_required
def institution_dashboard_view(request):
    """Displays the dashboard for the Institution Admin, listing its departments."""
    # Find the institution managed by the logged-in admin user
    try:
        # Check if the user is in the Institution_Admin group
        if not request.user.groups.filter(name='Institution_Admin').exists() and not request.user.is_superuser:
            return render(request, 'frontend/error.html', {'message': 'Access Denied: You must be an Institution Admin.'})

        institution = Institution.objects.get(admin_user=request.user)
    except Institution.DoesNotExist:
        # Handle cases where the user isn't an admin of any institution
        return render(request, 'frontend/error.html', {'message': 'You are not an administrator for any institution or your institution is not yet approved.'})

    # Get all departments belonging to this institution
    departments = Department.objects.filter(institution=institution).order_by('name')
    
    context = {
        'institution': institution,
        'departments': departments,
    }
    return render(request, 'frontend/institution_dashboard.html', context)

@login_required
def create_department_view(request):
    """Handles the creation of a new department by the Institution Admin."""
    if request.method == 'POST':
        department_name = request.POST.get('department_name')
        duration = request.POST.get('duration_years')
        
        # Get the institution managed by the current admin user
        try:
            institution = Institution.objects.get(admin_user=request.user)
        except Institution.DoesNotExist:
            return render(request, 'frontend/error.html', {'message': 'Institution not found.'})
            
        Department.objects.create(
            name=department_name,
            duration_years=duration,
            institution=institution
        )
        return redirect('institution_dashboard')
        
    return render(request, 'frontend/create_department.html')

@login_required
def assign_head_view(request, dept_id):
    """Handles assigning a new user as the Department Head."""
    try:
        department = Department.objects.get(id=dept_id)
    except Department.DoesNotExist:
        return render(request, 'frontend/error.html', {'message': 'Department not found.'})

    # Optional: Security check to ensure the department belongs to the admin's institution
    try:
        admin_institution = Institution.objects.get(admin_user=request.user)
        if department.institution != admin_institution:
            return render(request, 'frontend/error.html', {'message': 'Access Denied: You do not manage this department.'})
    except Institution.DoesNotExist:
        return render(request, 'frontend/error.html', {'message': 'Institution not found for the admin user.'})

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            # If the user already exists, assign them as head and redirect
            head_user = User.objects.get(username=username)
        else:
            # Create the new user for the Department Head
            head_user = User.objects.create_user(username=username, email=email, password=password)
        
        # Add them to the 'Department_Head' group
        dept_head_group, _ = Group.objects.get_or_create(name='Department_Head')
        head_user.groups.add(dept_head_group)
        
        # Assign this new user as the head of the department
        department.head = head_user
        department.save()
        
        return redirect('institution_dashboard')

    context = {
        'department': department
    }
    return render(request, 'frontend/assign_head.html', context)