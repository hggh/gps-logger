import secrets


from django.contrib.gis.db import models
from django_extensions.db.models import TimeStampedModel


class DevicePosition(TimeStampedModel):
    device = models.ForeignKey("logger.Device", on_delete=models.CASCADE, related_name='positions')
    location = models.PointField()
    altitude = models.FloatField(null=False, blank=False)
    datetime = models.DateTimeField(db_index=True, null=False, blank=False)
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.location}"

    class Meta:
        ordering = ('device', 'datetime',)
