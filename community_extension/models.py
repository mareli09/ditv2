from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    section = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.username} ({self.role})"


# Models related to CESO activities
class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    tags = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_activities')

    def __str__(self):
        return self.title


class Participation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity.title}"


class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    issued_on = models.DateField(auto_now_add=True)
    file_path = models.CharField(max_length=512)

    def __str__(self):
        return f"Certificate: {self.user.username} - {self.activity.title}"
