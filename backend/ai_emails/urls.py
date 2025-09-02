from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmailMessageListView.as_view(), name='email-list'),
    path('fetch/', views.FetchEmailsView.as_view(), name='fetch-emails'),
]