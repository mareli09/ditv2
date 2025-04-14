from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages
from .models import CustomUser
from django.http import HttpResponseRedirect
#from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

# Static pages
def home(request):
    return render(request, 'landing_page.html')

#login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting login with username: {username}")  # DEBUG

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"User authenticated: {user.username}, role: {user.role}, active: {user.is_active}")  # DEBUG
            auth_login(request, user)
            role = getattr(user, 'role', 'student')

            if role == 'student':
                return redirect(reverse('student_dashboard'))
            elif role == 'faculty':
                return redirect(reverse('faculty_dashboard'))
            elif role == 'ceso_staff':
                return redirect(reverse('cesostaff_dashboard'))
            elif role == 'it_staff':
                return redirect(reverse('it_dashboard'))
            else:
                return redirect(reverse('home'))
        else:
            print("Authentication failed.")  # DEBUG
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

#logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Dynamic and role-based views
@login_required
def dashboard(request):
    role = getattr(request.user, 'role', 'student')
    if role == 'student':
        return redirect('student_dashboard')
    elif role == 'faculty':
        return redirect('faculty_dashboard')
    elif role == 'admin':
        return redirect('cesostaff_dashboard')
    elif role == 'it_staff':
        return redirect('it_dashboard')
    else:
        return redirect('home')

@login_required
def activity_history(request):
    return render(request, 'activity_history.html')

@login_required
def activity_feedback(request):
    return render(request, 'activity_feedback.html')

@login_required
def certifications(request):
    return render(request, 'certifications.html')

@login_required
def sentiment_report(request):
    return render(request, 'sentiment_report.html')

@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def create_activity(request):
    return render(request, 'create_activity.html')

@login_required
def student_dashboard(request):
    return render(request, 'dashboard/student_dashboard.html')

@login_required
def faculty_dashboard(request):
    return render(request, 'dashboard/faculty_dashboard.html')

@user_passes_test(lambda u: u.is_authenticated and u.role == 'ceso_staff')
def cesostaff_dashboard(request):
    return render(request, 'dashboard/cesostaff_dashboard.html')

@login_required
def activities(request):
    return render(request, 'activities/list.html')

@login_required
def view_activity(request, activity_id):
    return render(request, 'activities/view.html')

@login_required
def submit_feedback(request):
    pass

@login_required
def certificates(request):
    return render(request, 'certificates/list.html')

def community_feedback(request, token):
    return render(request, 'community_feedback.html')

# IT staff dashboard and management
@user_passes_test(lambda u: u.is_authenticated and u.role == 'it_staff')
def it_dashboard(request):
    users = CustomUser.objects.all().order_by('-created_at')
    return render(request, 'dashboard/it_dashboard.html', {'users': users})

@user_passes_test(lambda u: u.is_authenticated and u.role == 'it_staff')
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"{user.username}'s status updated to {'Active' if user.is_active else 'Inactive'}")
    return redirect('it_dashboard')

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        status = request.POST.get('status', 'active')
        id_number = request.POST.get('id_number')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department', '')
        section = request.POST.get('section', '')
        course = request.POST.get('course', '')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                role=role,
                status=status,
                id_number=id_number,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                department=department,
                section=section,
                course=course,
                is_active=(status == 'active'),
            )
            messages.success(request, 'User account created successfully!')

        return redirect('it_dashboard')

    return render(request, 'add_user.html')
