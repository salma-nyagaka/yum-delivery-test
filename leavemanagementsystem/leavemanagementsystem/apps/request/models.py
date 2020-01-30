from django.db import models

from leavemanagementsystem import settings
from leavemanagementsystem.helpers.fancy_generator import fancy_id_generator


class Request(models.Model):
    id = models.CharField(db_index=True,
                          max_length=256,
                          default=fancy_id_generator,
                          primary_key=True,
                          editable=False)
    leave_request = models.CharField(default="Pending", max_length=200)
    requestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="request",
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_days = models.CharField(default="0", max_length=256, blank=True)

    @staticmethod
    def get_request_by_id(request_id):
        request = Request.objects.get(id=request_id)
        return request
