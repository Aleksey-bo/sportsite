from django.urls import path
from .views import (
    CreateUserView,
    GetCurrentUser
)

urlpatterns = [
    path('user/register/', CreateUserView.as_view()),
    path('current_user/', GetCurrentUser.as_view())
]