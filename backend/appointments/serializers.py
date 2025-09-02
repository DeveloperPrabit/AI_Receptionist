from rest_framework import serializers
from .models import Appointment, CalendarEvent

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class CalendarEventSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    
    class Meta:
        model = CalendarEvent
        fields = '__all__'
        read_only_fields = ('id', 'created_at')