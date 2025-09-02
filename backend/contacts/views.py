from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer

class ContactSubmissionCreateView(generics.CreateAPIView):
    serializer_class = ContactSubmissionSerializer
    permission_classes = []  # Allow anyone to submit contact forms
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Thank you for your message. We will get back to you soon.'},
            status=status.HTTP_201_CREATED, 
            headers=headers
        )