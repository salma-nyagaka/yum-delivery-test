from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny


from .serializers import NotificationSerializer
from .models import Notification
from leavemanagementsystem.apps.notifications.email import send_email
from leavemanagementsystem.apps.authentication.models import User
from leavemanagementsystem.apps.authentication.renderers import \
    UserJSONRenderer
from leavemanagementsystem.helpers.endpoint_response import \
    get_success_responses
from leavemanagementsystem.apps.authentication.backends import \
    JWTAuthentication
from leavemanagementsystem.apps.request.models import Request


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
            notification = Notification.objects.filter(
                id=notification_id).first()
            # pdb.set_trace()
            if notification:
                notification.status = "Accepted"
                notification.save()
                # pdb.set_trace()

                username = User.objects.values_list('username', flat=True).filter(
                    id=notification.leave_requestor_id).first()
                email = User.objects.values_list('email', flat=True).filter(
                    id=notification.leave_requestor_id).first()
                start_date = Request.objects.values_list(
                    'start_date', flat=True).filter(id=notification.request_id).first()
                end_date = Request.objects.values_list(
                    'end_date', flat=True).filter(id=notification.request_id).first()
                leave_status = Notification.objects.values_list(
                    'status', flat=True).filter(id=notification.id).first()

                send_email(
                    request, username, email, start_date,  end_date, leave_status
                )
                message = {
                    "message": "This leave request has been accepted.",
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
                status=status.HTTP_404_NOT_FOUND)


class DeclineRequestAPIView(APIView):
    """
    Class to decline a leave request
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, notification_id):
        if request.user.is_superuser:
            notification = Notification.objects.filter(
                id=notification_id).first()
            if notification:
                notification.status = "Declined"
                notification.save()

                username = User.objects.values_list('username', flat=True).filter(
                    id=notification.leave_requestor_id).first()
                email = User.objects.values_list('email', flat=True).filter(
                    id=notification.leave_requestor_id).first()
                start_date = Request.objects.values_list(
                    'start_date', flat=True).filter(id=notification.request_id).first()
                end_date = Request.objects.values_list(
                    'end_date', flat=True).filter(id=notification.request_id).first()
                leave_status = Notification.objects.values_list(
                    'status', flat=True).filter(id=notification.id).first()

                send_email(
                    request, username, email, start_date,  end_date, leave_status
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
                status=status.HTTP_404_NOT_FOUND)


class NotificationActivationAPIView(GenericAPIView):
    """Activate a user after mail verification."""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get(self, request, token, *args, **kwargs):
        """ Method for getting user token and activating them. """
        # After a successful registration, a user is activated through here
        # The token that was created and sent is decoded to get the user
        # The user's is_active attribute is then set to true
        try:
            data = JWTAuthentication.decode_jwt(token)
            user = User.objects.get(username=data['userdata'])
        except Exception:
            return Response(
                data={"message": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:8000/api/users/verified')
