from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout


# Static pages
def home(request):
    return render(request, 'landing_page.html')


#login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Login attempt:", username, password)  # Debug
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Login successful:", user.username, user.role)  # Debug
            auth_login(request, user)
            role = getattr(user, 'role', 'student')  # Ensure the 'role' field exists in your custom user model
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'faculty':
                return redirect('faculty_dashboard')
            elif role == 'admin':
                return redirect('cesostaff_dashboard')
        else:
            print("Login failed")  # Debug
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
    role = getattr(request.user, 'role', 'student')  # Ensure the 'role' field exists in your custom user model
    if role == 'student':
        return redirect('student_dashboard')
    elif role == 'faculty':
        return redirect('faculty_dashboard')
    elif role == 'admin':
        return redirect('cesostaff_dashboard')
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

@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
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
