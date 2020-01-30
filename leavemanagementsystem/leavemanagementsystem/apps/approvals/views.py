from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from leavemanagementsystem.helpers.endpoint_response import \
    get_success_responses
from rest_framework.views import APIView

from .models import AcceptedNotifications


class AcceptedAPIView(APIView):
    """
    Class to get all notifications
    """
    serializer_class = AcceptedNotifications
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        accepted_notifications = AcceptedNotifications.objects.all()
        for accepted in accepted_notifications:
            # pdb.set_trace()
            leave_data = {
                "id": accepted.notification.id,
                "notification": accepted.notification.notification,
                "email": accepted.notification.email,
                "start_date": accepted.notification.start_date,
                "end_date": accepted.notification.end_date,
                "description": accepted.notification.description,
                "number_of_days": accepted.notification.number_of_days
            }

            if request.user.is_superuser:
                return get_success_responses(
                    data=leave_data,
                    message="All accepted requests have been successfully\
                        retrieved",
                    status_code=status.HTTP_200_OK
                )
            else:
                return Response({
                    "error": "You are not allowed to view this content"},
                    status=status.HTTP_404_NOT_FOUND)


class AcceptRequestAPIView(APIView):
    """
    Class to accept a leave request
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, notification_id):
        if request.user.is_superuser:
            # pdb.set_trace()
            notification = AcceptedNotifications.objects.filter(
                notification_id=notification_id).first()
            if notification:
                notification.status = "Accepted"
                notification.save()

                message = {
                    "message": "This leave request has been accepted.",
                    "status": "successfully sent an email notification to\
                         the user"
                }
                return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "You are not allowed to perform this action"},
                status=status.HTTP_404_NOT_FOUND)


class DeclineRequestAPIView(APIView):
    """
    Class to decline a leave request
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, notification_id):
        if request.user.is_superuser:
            notification = AcceptedNotifications.objects.filter(
                notification_id=notification_id).first()
            if notification:
                notification.status = "Declined"
                notification.save()

                message = {
                    "message": "This leave request has been declined.",
                    "status": "Successfully sent an email notification\
                         to the user"
                }
                return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "You are not allowed to perform this action"},
                status=status.HTTP_404_NOT_FOUND)
