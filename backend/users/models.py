from django.contrib.auth.models import User
from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    preferences = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def encrypt_field(self, value):
        if value:
            return settings.cipher_suite.encrypt(value.encode()).decode()
        return value
    
    def decrypt_field(self, value):
        if value:
            return settings.cipher_suite.decrypt(value.encode()).decode()
        return value
    
    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = self.encrypt_field(self.phone)
        super().save(*args, **kwargs)
    
    def get_phone(self):
        return self.decrypt_field(self.phone)
    
    def __str__(self):
        return self.user.username