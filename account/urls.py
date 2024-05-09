from django.urls import path
from .views import (
    RegistrationAPIView,
    GetCurrentUser
)

urlpatterns = [
    path('user/register/', RegistrationAPIView.as_view()),
    path('current_user/', GetCurrentUser.as_view())
]