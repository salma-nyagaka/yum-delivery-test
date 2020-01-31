from rest_framework import status
from rest_framework.generics import GenericAPIView
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.dispatch import receiver
from django.db.models.signals import post_save

from .serializers import RequestSerializer
from leavemanagementsystem.helpers.endpoint_response import \
    get_success_responses
from ..notifications.models import request_notification
from leavemanagementsystem.apps.authentication.models import \
    User
from .models import Request


@receiver(post_save, sender=Request)
def notify_manager(sender, instance, created, **kwargs):
    """
    Method to send a message notification
    upon creation of a request.
    """
    if created:
        user_id = instance.requestor_id
        username = User.objects.filter(id=user_id).values_list(
            'username', flat=True).first()
        message = (" This leave request has been made by {}".format(username))
        leave_start_date = instance.start_date
        leave_end_date = instance.end_date
        leave_description = instance.description
        number_of_days = instance.number_of_days
        email = User.objects.filter(id=user_id).values_list(
            'email', flat=True).first()
        request_notification(message, instance, email, user_id,
                             leave_start_date, leave_end_date,
                             leave_description, number_of_days)


class RequestAPIView(GenericAPIView):
    """Class for handling the request"""

    permission_classes = (IsAuthenticated,)
    serializer_class = RequestSerializer

    def post(self, request):
        """Method for making a leave request"""
        start_date, end_date, description, = request.data.get(
            'start_date', None), request.data.get(
            'end_date', None), request.data.get('description', None),

        string_input_with__start_date = request.data.get('start_date', None)
        start = datetime.strptime(string_input_with__start_date, "%Y-%m-%d")
        present = datetime.now()
        start_date_validation = start.date() < present.date()
        string_input_with__end_date = request.data.get('end_date', None)
        end = datetime.strptime(string_input_with__end_date, "%Y-%m-%d")
        end_date_validation = end.date() < present.date()

        leave_duration = end - start
        request_data = {
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "requestor": request.user.id,
            "number_of_days": leave_duration.days
        }
        request_data

        context = {'request': request}
        serializer = self.serializer_class(data=request_data, context=context)
        serializer.is_valid(raise_exception=True)

        saved_request = serializer.save()

        if start_date_validation or end_date_validation:
            return Response({"message": "The date selected should be more \
                than today"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif end < start:
            return Response({"message": "End date of leave should be greator \
                than start date of the leave requested"},
                            status=status.HTTP_400_BAD_REQUEST)

        return get_success_responses(
            data={
                "id": saved_request.id,
                "requestor": request.user.id,
                "start_date": saved_request.start_date,
                "end_date": saved_request.end_date,
                "description": saved_request.description,
                "number_of_days": saved_request.number_of_days
            },
            message="Your request has been successfully sent to the admin",
            status_code=status.HTTP_201_CREATED
        )

    def get(self, request):
        """Method for getting all requests"""
        requests_made = Request.objects.filter(requestor_id=request.user.id)
        serializer = RequestSerializer(requests_made, many=True)

        return get_success_responses(
            data=serializer.data,
            message="All requests have been retrieved successfully",
            status_code=status.HTTP_200_OK
        )


class SingleRequestAPIView(GenericAPIView):
    """Class for handling a single user request"""

    permission_classes = (IsAuthenticated,)
    serializer_class = RequestSerializer

    def get(self, request, request_id):
        """Method for getting one request detail."""

        # import pdb
        # pdb.set_trace()
        try:
            request_made = Request.get_request_by_id(request_id=request_id)
            request_data = {
                "id": request_made.id,
                "requestor": request_made.id,
                "start_date": request_made.start_date,
                "end_date": request_made.end_date,
                "description": request_made.description,
            }
            return get_success_responses(
                data=request_data,
                message="Leave request details successfully fetched.")
        except Exception:
            return Response({'message': "Leave request not found."},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, request_id):
        """Method for deleting a specific leave request."""
        try:
            leave_request = Request.get_request_by_id(request_id=request_id)
            if leave_request:
                if request.user.id != leave_request.requestor_id:
                    message = {
                        'error': "You are not allowed to delete these details."}  # noqa E501
                    return Response(message,
                                    status=status.HTTP_403_FORBIDDEN)
            leave_request.delete()
            message = {
                'message': "You have successfully deleted your leave request"
            }
            return Response(message, status=status.HTTP_200_OK)

        except Exception:
            return Response({'message': "Leave request not found."},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, request_id):
        """Method for editing leave request details."""
        try:
            leave_request = Request.get_request_by_id(request_id=request_id)
            if request.user.id != leave_request.requestor_id:
                return Response(
                    {'error': "You are not allowed to perform this action."},
                    status=status.HTTP_403_FORBIDDEN)

            data = request.data
            serializer = RequestSerializer(instance=leave_request, data=data,
                                           partial=True)
            serializer.is_valid(raise_exception=True)
            request_made = serializer.save()
            response_data = {
                "id": request_made.id,
                "requestor": request_made.id,
                "start_date": request_made.start_date,
                "end_date": request_made.end_date,
                "leave_request": request_made.leave_request,
                "description": request_made.description,
            }

            return get_success_responses(
                data=response_data,
                message="Your details have been successfully updated.",
                status_code=status.HTTP_200_OK
            )
        except (KeyError, Request.DoesNotExist):
            return Response({
                "error": "The leave request does not exist"},
                status=status.HTTP_404_NOT_FOUND)
