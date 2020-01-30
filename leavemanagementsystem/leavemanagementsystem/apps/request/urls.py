from django.urls import path

from .views import RequestAPIView, SingleRequestAPIView

app_name = "request"

urlpatterns = [
    path('request', RequestAPIView.as_view(),
         name='request'),
    path('request/<str:request_id>', SingleRequestAPIView.as_view(),
         name='request_made'),
]
