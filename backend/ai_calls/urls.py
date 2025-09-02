from django.urls import path
from . import views

urlpatterns = [
    path('', views.CallRecordListView.as_view(), name='call-list'),
    path('start/', views.StartCallView.as_view(), name='start-call'),
    path('twilio-webhook/', views.TwilioWebhookView.as_view(), name='twilio-webhook'),
]