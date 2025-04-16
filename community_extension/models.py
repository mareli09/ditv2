from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('ceso_staff', 'CESO Staff'),
        ('it_staff', 'IT Staff'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    id_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150)
    department = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Models related to CESO activities
"""
#error due to duplicate 
class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    tags = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_activities')

    def __str__(self):
        return self.title
"""

class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    conducted_by = models.CharField(max_length=255, blank=True, null=True)
    fees_expenses = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    attachment = models.FileField(upload_to='activity_attachments/', blank=True, null=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Participation(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity.title}"


class Certificate(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    issued_on = models.DateField(auto_now_add=True)
    file_path = models.CharField(max_length=512)

    def __str__(self):
        return f"Certificate: {self.user.username} - {self.activity.title}"



class ActivityLog(models.Model):
    actor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='actions')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    affected_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='logs')

    def __str__(self):
        return f"{self.timestamp}: {self.actor} -> {self.action}"
    
"""
class Activity(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    conducted_by = models.CharField(max_length=255)
    fees_expenses = models.CharField(max_length=100)
    description = models.TextField()
    attachment = models.FileField(upload_to='activity_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
#this area is error and duplicate        
"""
