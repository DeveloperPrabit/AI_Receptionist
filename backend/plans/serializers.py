from rest_framework import serializers
from .models import Plan, Subscription, PaymentRecord

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('id', 'start_date')

class PaymentRecordSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)
    
    class Meta:
        model = PaymentRecord
        fields = '__all__'
        read_only_fields = ('id', 'created_at')