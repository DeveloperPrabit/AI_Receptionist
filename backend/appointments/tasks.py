from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Appointment

@shared_task
def send_appointment_reminders():
    # Find appointments happening in the next 24 hours
    now = timezone.now()
    tomorrow = now + timedelta(hours=24)
    
    upcoming_appointments = Appointment.objects.filter(
        start_time__gte=now,
        start_time__lte=tomorrow,
        status='scheduled'
    )
    
    for appointment in upcoming_appointments:
        # Send reminder email or SMS
        user = appointment.user.user
        message = f"Reminder: You have an appointment '{appointment.title}' scheduled for {appointment.start_time}."
        
        # In a real implementation, you would send an email or SMS here
        print(f"Sending reminder to {user.email}: {message}")
    
    return f"Sent {upcoming_appointments.count()} reminders"