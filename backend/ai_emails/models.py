from django.db import models
from users.models import UserProfile

class EmailMessage(models.Model):
    EMAIL_CATEGORY_CHOICES = [
        ('general', 'General'),
        ('urgent', 'Urgent'),
        ('spam', 'Spam'),
        ('appointment', 'Appointment'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.EmailField()
    category = models.CharField(max_length=20, choices=EMAIL_CATEGORY_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Email from {self.sender}: {self.subject}"

class EmailThread(models.Model):
    emails = models.ManyToManyField(EmailMessage, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Thread with {self.emails.count()} emails"