from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from logger.models import Device, DevicePub


class IndexView(TemplateView):
    template_name = 'index.html'


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'


class DevicePubView(TemplateView):
    template_name = 'device_pub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if slug is None:
            context['error'] = True
            return context
        try:
            device_pub = DevicePub.objects.get(slug=slug)
        except ObjectDoesNotExist:
            context['error'] = True
            return context

        if device_pub.is_active():
            context['device'] = device_pub.device
            context['device_pub'] = device_pub
        else:
            context['error'] = True

        return context


class DevicePositionUploadView(TemplateView):
    def get(self, request, *args, **kwargs):
        token = request.headers.get('token', None)
        if token is None:
            return HttpResponse(content='Token Header missing or not found.')
        try:
            device = Device.objects.get(token=token)
        except ObjectDoesNotExist:
            return HttpResponse(content='Token Header missing or not found.')

        request_data = request.GET.copy()

        needed_headers = ['lat', 'lon', 'alt', 'time']
        for h in needed_headers:
            if h not in request_data:
                return HttpResponse(status_code='404', content=f'GET Parameter {h} not found in {request_data}')

        device.upload_point(request_data)

        return HttpResponse(content='OK')
