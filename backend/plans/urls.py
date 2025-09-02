from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlanListView.as_view(), name='plan-list'),
    path('stripe-checkout/', views.CreateStripeCheckoutSessionView.as_view(), name='stripe-checkout'),
    path('stripe-webhook/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
]