from django.urls import path
from .views import (
    RegistrationAPIView,
    GetCurrentUser,
    GetUserProduct,
    GetUserChat
)

urlpatterns = [
    path('user/register/', RegistrationAPIView.as_view(), name='registration'),
    path('current_user/', GetCurrentUser.as_view()),
    path('get_user_products/', GetUserProduct.as_view()),
    path('get_user_chat/', GetUserChat.as_view())
]