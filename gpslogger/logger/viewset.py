from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django.core.exceptions import ObjectDoesNotExist

from logger.models import Device, DevicePub


class DevicePubViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['GET',])
    def last_pos(self, request, pk=None):
        try:
            device_pub = DevicePub.objects.get(slug=pk)
        except ObjectDoesNotExist:
            return Response({}, status=404)

        if device_pub.is_active() is False:
            return Response({}, status=404)

        return Response(device_pub.device.get_last_position())

    @action(detail=True, methods=['GET',])
    def geojson_track(self, request, pk=None):
        try:
            device_pub = DevicePub.objects.get(slug=pk)
        except ObjectDoesNotExist:
            return Response({}, status=404)

        if device_pub.is_active() is False:
            return Response({}, status=404)

        return Response(device_pub.device.get_last_geojson_track())
