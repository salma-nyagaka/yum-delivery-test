from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from leavemanagementsystem.helpers.endpoint_response import \
    get_success_responses
from rest_framework.views import APIView

from .models import AcceptedNotifications
from .serializers import AcceptedNotificationsSerializer
from leavemanagementsystem.apps.approvals.email import \
    send_email
from leavemanagementsystem.apps.notifications.models import \
    Notification
from leavemanagementsystem.apps.authentication.models import User
from leavemanagementsystem.apps.role.models import Role


class AcceptedAPIView(APIView):
    """
    Class to get all notifications
    """
    serializer_class = AcceptedNotifications
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Method to get all the accepted requests from manager
        """
        requests_made = AcceptedNotifications.objects.all()
        serializer = AcceptedNotificationsSerializer(requests_made,
                                                     many=True)
        role = request.user.role_id
        role_status = Role.objects.filter(
            id=role).values_list('title', flat=True)[0]

        if request.user.is_superuser and role_status == 'HR':

            return get_success_responses(
                data=serializer.data,
                message="All requests have been retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        else:
            return Response({
                "error": "Only the HR can view this content"},
                status=status.HTTP_403_FORBIDDEN)


class AcceptRequestAPIView(APIView):
    """
    Class to accept a leave request by HR
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, notification_id):
        """
        Method to acceptleave request and
        send emeail notification to the user
        """
        role = request.user.role_id
        role_status = Role.objects.filter(
            id=role).values_list('title', flat=True)[0]

        if request.user.is_superuser and role_status == 'HR':
            notification = AcceptedNotifications.objects.filter(
                notification_id=notification_id).first()
            if notification:
                notification.status = "accepted"
                notification.save()

                user_id = Notification.objects.filter(
                    id=notification_id).values_list(
                    'leave_requestor_id', flat=True)[0]
                username = User.objects.filter(
                    id=user_id).values_list('username', flat=True)[0]

                message = {
                    "message": "This leave request has been accepted.",
                    "status": "successfully sent an email notification to\
                    the user"
                }

                email = Notification.objects.filter(
                    id=notification_id).values_list('email', flat=True)[0]
                start_date = Notification.objects.filter(
                    id=notification_id).values_list('start_date', flat=True)[0]
                end_date = Notification.objects.filter(
                    id=notification_id).values_list('end_date', flat=True)[0]
                status_update = notification.status

                send_email(request, username, email,
                           start_date, end_date, status_update)
                return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Only the HR can perform this action"},
                status=status.HTTP_403_FORBIDDEN)


class DeclineRequestAPIView(APIView):
    """
    Class to decline a leave request by HR
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, notification_id):
        """
        Method to acceptleave request and
        send emeail notification to the user
        """
        role = request.user.role_id
        role_status = Role.objects.filter(
            id=role).values_list('title', flat=True)[0]

        if request.user.is_superuser and role_status == 'HR':
            notification = AcceptedNotifications.objects.filter(
                notification_id=notification_id).first()
            if notification:
                notification.status = "declined"
                notification.save()
                user_id = Notification.objects.filter(
                    id=notification_id).values_list(
                    'leave_requestor_id', flat=True)[0]
                username = User.objects.filter(
                    id=user_id).values_list('username', flat=True)[0]

                message = {
                    "message": "This leave request has been declined.",
                    "status": "Successfully sent an email notification\
                         to the user"
                }
                email = Notification.objects.filter(
                    id=notification_id).values_list('email', flat=True)[0]
                start_date = Notification.objects.filter(
                    id=notification_id).values_list('start_date', flat=True)[0]
                end_date = Notification.objects.filter(
                    id=notification_id).values_list('end_date', flat=True)[0]
                status_update = notification.status

                send_email(request, username, email,
                           start_date, end_date, status_update)
                return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Only the HR can perform this action"},
                status=status.HTTP_403_FORBIDDEN)
