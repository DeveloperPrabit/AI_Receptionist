from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment, CalendarEvent
from .serializers import AppointmentSerializer, CalendarEventSerializer

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user.userprofile)

class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user.userprofile)