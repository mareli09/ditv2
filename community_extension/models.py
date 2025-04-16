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
    department = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


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


class GuestFeedback(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='guest_feedbacks')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.activity.title}"


class Certificate(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='issued_certificates')
    date_issued = models.DateField(auto_now_add=True)
    description = models.TextField(default="Certificate of Participation in the community outreach program.")
    file = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"Certificate for {self.user} in {self.activity.title}"


class ActivityLog(models.Model):
    actor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='actions')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    affected_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='logs')

    def __str__(self):
        return f"{self.timestamp}: {self.actor} -> {self.action}"
