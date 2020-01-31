from django.db import models

from leavemanagementsystem.helpers.fancy_generator import fancy_id_generator
from ..notifications.models import Notification


class AcceptedNotifications(models.Model):
    """
    Database fields for the accepted requests from the manager
    """
    id = models.CharField(db_index=True,
                          max_length=256,
                          default=fancy_id_generator,
                          primary_key=True,
                          editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    status = models.CharField(default="pending", max_length=100, blank=False)


def approval_notification(status, notification_id):
    """
    This function adds notification to the accpeted notification model
    """
    notification = AcceptedNotifications.objects.create(
        notification_id=notification_id)
    notification.save()
