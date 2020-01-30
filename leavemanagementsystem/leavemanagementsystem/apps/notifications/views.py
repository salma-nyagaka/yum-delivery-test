from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from leavemanagementsystem.helpers.endpoint_response import \
    get_success_responses
from rest_framework.views import APIView

from .serializers import NotificationSerializer
from .models import Notification

import pdb


class NotificationAPIView(APIView):
    """
    Class to get all notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        # pdb.set_trace()
        if request.user.is_superuser:
            return get_success_responses(
                data=serializer.data,
                message="All notifications have been successfully \
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
            notification = Notification.objects.filter(id=notification_id).first()
            if notification:
                notification.status = "Accepted"
                notification.save()

                message = {
                    "message": "This leaverequest has been accepted.",
                    "status": "success"
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
            notification = Notification.objects.filter(id=notification_id).first()
            if notification:
                notification.status = "Declined"
                notification.save()

                message = {
                    "message": "This request has been declined.",
                    "status": "success"
                }
                return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "You are not allowed to perform this action"},
                status=status.HTTP_404_NOT_FOUND)
