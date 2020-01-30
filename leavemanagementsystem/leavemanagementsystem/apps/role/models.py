from django.db import models

from leavemanagementsystem.helpers.fancy_generator import fancy_id_generator


class Role(models.Model):
    id = models.CharField(db_index=True,
                          max_length=256,
                          default=fancy_id_generator,
                          primary_key=True,
                          editable=False)
    title = models.CharField(max_length=256,
                             blank=True,
                             default='Regular User')
    description = models.CharField(max_length=256, blank=True)
