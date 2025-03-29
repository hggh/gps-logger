import secrets

from django.utils import timezone
from django.contrib.gis.db import models
from django_extensions.db.models import TimeStampedModel


def generate_slug_token():
    return secrets.token_urlsafe(30)


class DevicePub(TimeStampedModel):
    device = models.ForeignKey("Device", null=False, blank=False, related_name='pubs', on_delete=models.CASCADE)
    slug = models.SlugField(default=generate_slug_token, null=False, editable=False, max_length=50)
    valid_until = models.DateTimeField(null=False, blank=False)

    def is_active(self):
        return self.valid_until > timezone.now()

    def __str__(self):
        return f"{self.device.name} - {self.valid_until}"

    class Meta:
        ordering = ['device', 'valid_until', ]
