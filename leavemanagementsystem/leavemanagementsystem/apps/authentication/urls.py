from django.urls import path
from django.views.generic import TemplateView


from .views import (
    RegistrationAPIView,
    LoginAPIView,
    UserActivationAPIView)

app_name = "authentication"

urlpatterns = [
    path('users/register', RegistrationAPIView.as_view(),
         name='user_signup'),
    path('users/login', LoginAPIView.as_view(),
         name='user_login'),
    path('auth/<str:token>', UserActivationAPIView.as_view(),
         name='activate_user'),
    path('users/verified', TemplateView.as_view(
         template_name='account_verified.html'))
]
