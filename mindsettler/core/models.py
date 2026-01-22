from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Appointment(models.Model):
    SESSION_TYPES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES, default='ONLINE')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    google_event_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.start_time} ({self.status})"
