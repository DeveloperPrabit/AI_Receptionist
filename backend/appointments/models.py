from django.db import models
from users.models import UserProfile

class Appointment(models.Model):
    APPOINTMENT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='appointments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} for {self.user.user.username} at {self.start_time}"

class CalendarEvent(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='calendar_event')
    event_id = models.CharField(max_length=255)  # ID from Google Calendar or other service
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Calendar event for {self.appointment.title}"