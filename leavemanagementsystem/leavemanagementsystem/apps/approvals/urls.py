from django.urls import path

from .views import AcceptedAPIView, AcceptRequestAPIView, DeclineRequestAPIView

app_name = 'approvals'

urlpatterns = [
    path('notifications/accepted', (AcceptedAPIView.as_view()),
         name='accepted_notifications'),
    path('notifications/hr/accept/<str:notification_id>',
         (AcceptRequestAPIView.as_view()),
         name='accept_notifications'),
    path('notifications/hr/decline/<str:notification_id>',
         (DeclineRequestAPIView.as_view()),
         name='accept_notifications'),


]
