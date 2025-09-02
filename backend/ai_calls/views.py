from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CallRecord, CallTransfer
from .serializers import CallRecordSerializer, CallTransferSerializer
from .tasks import process_call_audio, initiate_call

class CallRecordListView(generics.ListAPIView):
    serializer_class = CallRecordSerializer
    
    def get_queryset(self):
        return CallRecord.objects.filter(user=self.request.user.userprofile)

class StartCallView(APIView):
    def post(self, request):
        to_number = request.data.get('to_number')
        
        if not to_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Initiate the call asynchronously
        call_sid = initiate_call.delay(to_number)
        
        return Response({'call_sid': call_sid, 'message': 'Call initiated'})

class TwilioWebhookView(APIView):
    def post(self, request):
        # Handle Twilio webhook for call status updates
        call_sid = request.POST.get('CallSid')
        call_status = request.POST.get('CallStatus')
        
        # Update call record based on status
        # This is a simplified implementation
        
        return Response({'status': 'received'})