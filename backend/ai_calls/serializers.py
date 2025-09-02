from rest_framework import serializers
from .models import CallRecord, CallTransfer

class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class CallTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallTransfer
        fields = '__all__'
        read_only_fields = ('id', 'created_at')