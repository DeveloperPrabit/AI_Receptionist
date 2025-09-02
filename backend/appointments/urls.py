from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment-list'),
    path('create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
]