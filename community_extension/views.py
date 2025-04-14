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
from django.db.models import Q
from django.core.paginator import Paginator


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
@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'it_staff')
def it_dashboard(request):
    users = CustomUser.objects.all().order_by('-created_at')

    # Count users by role
    active_users_count = users.filter(is_active=True).count()
    inactive_users_count = users.filter(is_active=False).count()
    student_count = users.filter(role='student').count()
    faculty_count = users.filter(role='faculty').count()
    ceso_count = users.filter(role='ceso_staff').count()
    it_count = users.filter(role='it_staff').count()

    return render(request, 'dashboard/it_dashboard.html', {
        'active_users_count': active_users_count,
        'inactive_users_count': inactive_users_count,
        'student_count': student_count,
        'faculty_count': faculty_count,
        'ceso_count': ceso_count,
        'it_count': it_count,
        'users': users,
    })

@user_passes_test(lambda u: u.is_authenticated and u.role == 'it_staff')
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
     # Log the toggle
    ActivityLog.objects.create(
        actor=request.user,
        action=f"Toggled user status for {user.username} to {'Active' if user.is_active else 'Inactive'}",
        affected_user=user
    )
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
            # Log the creation
            ActivityLog.objects.create(
                actor=request.user,
                action=f"Created user {user.username} ({user.role})",
                affected_user=user
            )

            messages.success(request, 'User account created successfully!')

        return redirect('it_dashboard')

    return render(request, 'add_user.html')


#for edit_user

@user_passes_test(lambda u: u.is_authenticated and u.role == 'it_staff')
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.status = request.POST.get('status')
        user.id_number = request.POST.get('id_number')
        user.first_name = request.POST.get('first_name')
        user.middle_name = request.POST.get('middle_name')
        user.last_name = request.POST.get('last_name')
        user.department = request.POST.get('department')
        user.section = request.POST.get('section')
        user.course = request.POST.get('course')
        user.is_active = (user.status == 'active')

        user.save()
        
        ActivityLog.objects.create(
            actor=request.user,
            action=f"Edited user {user.username}",
            affected_user=user
        )
        messages.success(request, 'User updated successfully!')
        return redirect('manage_users')

    return render(request, 'edit_user.html', {'user': user})

#for logs
@user_passes_test(lambda u: u.is_authenticated and u.role == 'it_staff')
def view_logs(request):
    logs = ActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/it_logs.html', {'logs': logs})

def manage_users(request):
    search = request.GET.get('search', '')
    role = request.GET.get('role', '')
    status = request.GET.get('status', '')

    users = CustomUser.objects.all()

    if search:
        users = users.filter(username__icontains=search)
    if role:
        users = users.filter(role=role)
    if status:
        users = users.filter(status=status)

    paginator = Paginator(users, 10)  # 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/manage_users.html', {
        'users': page_obj,
        'page_obj': page_obj
    })