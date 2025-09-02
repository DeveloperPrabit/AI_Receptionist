from rest_framework import serializers
from .models import EmailMessage, EmailThread

class EmailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessage
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class EmailThreadSerializer(serializers.ModelSerializer):
    emails = EmailMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = EmailThread
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')