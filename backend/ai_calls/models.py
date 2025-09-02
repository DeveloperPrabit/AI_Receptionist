from django.db import models
from users.models import UserProfile

class CallRecord(models.Model):
    CALL_STATUS_CHOICES = [
        ('answered', 'Answered'),
        ('missed', 'Missed'),
        ('transferred', 'Transferred'),
    ]
    
    caller_id = models.CharField(max_length=20)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='call_records')
    transcript = models.TextField(blank=True, null=True)
    duration = models.DurationField()
    status = models.CharField(max_length=20, choices=CALL_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Call from {self.caller_id} at {self.created_at}"

class CallTransfer(models.Model):
    TRANSFER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    call_record = models.OneToOneField(CallRecord, on_delete=models.CASCADE, related_name='transfer')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transferred_calls')
    status = models.CharField(max_length=20, choices=TRANSFER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transfer for call {self.call_record.id} to {self.to_user.user.username}"