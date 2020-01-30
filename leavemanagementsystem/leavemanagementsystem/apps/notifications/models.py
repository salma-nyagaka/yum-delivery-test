from django.db import models
from ..request.models import Request
from leavemanagementsystem.helpers.fancy_generator import fancy_id_generator
from leavemanagementsystem import settings
import pdb


class Notification(models.Model):
    """
    Database fields for the notifications
    """
    id = models.CharField(db_index=True,
                          max_length=256,
                          default=fancy_id_generator,
                          primary_key=True,
                          editable=False)
    leave_requestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="leave_requestor",
        on_delete=models.CASCADE,
    )
    request = models.ForeignKey(
        Request, blank=True, null=True, on_delete=models.CASCADE)
    notification = models.TextField()
    email = models.CharField(max_length=256, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=256, blank=True)
    classification = models.TextField(default="trip")
    status = models.CharField(default="Pending", max_length=256, blank=True)
    number_of_days = models.CharField(default="0", max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_notification_by_id(notification_id):
        notification = Notification.objects.get(id=notification_id)
        return notification

    def get_notification_request_id(request_id):
        request = Request.objects.get(id=request_id)
        return request


def request_notification(notification, request, email, user, start, end,
                         description):
    """
    This function adds notification to the Notification model
    Checks if the user is in the list to be notified
    """
    notification = Notification.objects.create(
        notification=notification, classification="request", request=request,
        leave_requestor_id=user, email=email, start_date=start,
        end_date=end, description=description)
    notification.save()
