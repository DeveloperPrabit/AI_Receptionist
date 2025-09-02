from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/calls/', include('ai_calls.urls')),
    path('api/emails/', include('ai_emails.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/plans/', include('plans.urls')),
]