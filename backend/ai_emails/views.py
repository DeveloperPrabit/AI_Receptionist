from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EmailMessage, EmailThread
from .serializers import EmailMessageSerializer, EmailThreadSerializer
from .tasks import process_incoming_email



class EmailMessageListView(generics.ListAPIView):
    serializer_class = EmailMessageSerializer
    
    def get_queryset(self):
        return EmailMessage.objects.filter(user=self.request.user.userprofile)

class FetchEmailsView(APIView):
    def post(self, request):
        email_account = request.data.get('email_account')
        password = request.data.get('password')
        
        if not email_account or not password:
            return Response({'error': 'Email account and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch emails asynchronously
        task = fetch_emails.delay(request.user.userprofile.id, email_account, password)
        
        return Response({'task_id': task.id, 'message': 'Email fetching started'})