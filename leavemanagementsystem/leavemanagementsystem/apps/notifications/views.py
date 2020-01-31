from rest_framework import status
from rest_framework.response import Response
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from .serializers import NotificationSerializer
from .models import Notification
from leavemanagementsystem.apps.notifications.email import send_email
from leavemanagementsystem.apps.authentication.models import User
from leavemanagementsystem.helpers.endpoint_response import \
    get_success_responses
from leavemanagementsystem.apps.request.models import Request
from leavemanagementsystem.apps.role.models import Role
from ..approvals.models import approval_notification


@receiver(post_save, sender=Notification)
def notify_hr(sender, instance, **kwargs):
    """
    send a message notification upon accepting a request.
    """
    notification_id = instance.id
    leave_status = instance.status
    approval_notification(leave_status, notification_id)


class NotificationAPIView(APIView):
    """
    Class to get all notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Method to get all leave requests
        """

        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        role = request.user.role_id
        role_status = Role.objects.filter(
            id=role).values_list('title', flat=True)[0]

        if request.user.is_superuser and role_status == 'Manager':
            return get_success_responses(
                data=serializer.data,
                message="All notifications have been successfully \
                    retrieved",
                status_code=status.HTTP_200_OK
            )
        else:
            return Response({
                "error": "Only the HR can view this content"},
                status=status.HTTP_403_FORBIDDEN)


class AcceptRequestAPIView(APIView):
    """
    Class to accept a leave request
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, notification_id):
        """
        Method to accept leave requests
        """
        role = request.user.role_id
        role_status = Role.objects.filter(
            id=role).values_list('title', flat=True)[0]

        if request.user.is_superuser and role_status == 'Manager':
            notification = Notification.objects.filter(
                id=notification_id).first()
            if notification:
                notification.status = "accepted"
                notification.save()

                message = {
                    "message": "This leave request has been accepted.",
                    "status": "The HR department will proceed with\
                         the leave request process"
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Leave request notification not found"},
                    status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({
                "error": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN)


class DeclineRequestAPIView(APIView):
    """
    Class to decline a leave request
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, notification_id):
        """
        Method to decline leave requests
        """
        role = request.user.role_id
        role_status = Role.objects.filter(
            id=role).values_list('title', flat=True)[0]

        if request.user.is_superuser and role_status == 'Manager':
            notification = Notification.objects.filter(
                id=notification_id).first()
            if notification:
                notification.status = "declined"
                notification.save()

                username = User.objects.values_list(
                    'username', flat=True).filter(
                        id=notification.leave_requestor_id).first()
                email = User.objects.values_list(
                    'email', flat=True).filter(
                        id=notification.leave_requestor_id).first()
                start_date = Request.objects.values_list(
                    'start_date', flat=True).filter(
                        id=notification.request_id).first()
                end_date = Request.objects.values_list(
                    'end_date', flat=True).filter(
                        id=notification.request_id).first()
                leave_status = Notification.objects.values_list(
                    'status', flat=True).filter(
                        id=notification.id).first()

                send_email(
                    request, username, email, start_date,  end_date,
                    leave_status
                )

                message = {
                    "message": "This request has been declined.",
                    "status": "success"
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Leave request notification not found"},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "error": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN)
