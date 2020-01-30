from django.urls import path

from .views import NotificationAPIView, AcceptRequestAPIView, DeclineRequestAPIView

app_name = 'notification'

urlpatterns = [
    path('notifications', (NotificationAPIView.as_view()),
         name='all_notifications'),
    path('notifications/accept/<str:notification_id>',
         (AcceptRequestAPIView.as_view()),
         name='accept_notification'),
    path('notifications/decline/<str:notification_id>',
         (DeclineRequestAPIView.as_view()),
         name='decline_notification'),
]
