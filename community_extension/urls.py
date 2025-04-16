from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Role-based dashboards
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/cesostaff/', views.cesostaff_dashboard, name='cesostaff_dashboard'),

    # Activities
    path('activities/', views.activities, name='activities'),
    path('activities/create/', views.update_activity, name='create_activity'),  # Create activity
    path('activities/<int:activity_id>/', views.view_activity, name='view_activity'),
    #for edit
    path('activities/<int:id>/edit/', views.update_activity, name='update_activity'),
    # Feedback
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),

    # Certificates
    path('certificates/', views.certificates, name='certificates'),

    # Community portal
    path('community/feedback/<str:token>/', views.community_feedback, name='community_feedback'),
    
    #logoutview
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # IT Staff
    path('dashboard/it/', views.it_dashboard, name='it_dashboard'),
    path('dashboard/it/manage-users/', views.manage_users, name='manage_users'),
    path('dashboard/it/add-user/', views.add_user, name='add_user'),
    path('dashboard/it/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/it/logs/', views.view_logs, name='view_logs'),
    path('dashboard/it/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    
    #for csv
    path('download-csv/', views.download_users_csv, name='download_users_csv'),
    
    #ceso create activity 
    path('create-activity/', views.create_activity, name='create_activity')

]

# Add this to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)