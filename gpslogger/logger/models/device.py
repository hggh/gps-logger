import secrets
import geojson

from django.utils import timezone
from django.contrib.gis.geos import Point
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel


def generate_slug_token():
    return secrets.token_urlsafe(30)


class Device(TimeStampedModel):
    name = models.CharField(null=False, blank=False)
    token = models.SlugField(default=generate_slug_token, null=False, editable=False, max_length=50, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)

    def upload_point(self, data):
        from .device_position import DevicePosition

        items = {}
        for k in ['lat', 'lon', 'alt', 'time']:
            items[k] = data.get(k)
            del data[k]

        pos = DevicePosition(
            device=self,
            location=Point([float(items.get('lat')), float(items.get('lon'))], srid=4326),
            altitude=float(items.get('alt')),
            datetime=items.get('time'),
            data=data,
        )
        pos.full_clean()
        pos.save()

    def get_last_position_datetime(self):
        if self.positions.all().last():
            return self.positions.all().last().datetime

        return None

    def get_last_position(self):
        pos = self.positions.all().last()

        return {
            'lat': pos.location[0],
            'long': pos.location[1],
            'datetime': str(pos.datetime),
        }

    def get_last_geojson_track(self, hours=30):
        coordinates = []
        for pos in self.positions.all().filter(datetime__gt=timezone.now() - timezone.timedelta(hours=hours)):
            pos = pos.location
            coordinates.append([pos[1], pos[0]])

        fc = geojson.FeatureCollection(features=[])
        fc.features.append(geojson.Feature(
            geometry=geojson.LineString(coordinates=coordinates),
            properties={
                'color': '#448137',
                'weight': 3,
                'opacity': 0.7,
            }
        ))

        return fc

    def seen_recently_minutes(self):
        return 120

    def seen_recently(self):
        return self.positions.all().filter(datetime__gt=timezone.now() - timezone.timedelta(minutes=self.seen_recently_minutes())).exists()

    def __str__(self):
        return f"{self.owner.username}/{self.name}"

    class Meta:
        ordering = ('owner', 'name',)
