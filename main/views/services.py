from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, get_list_or_404
from main import models, mixins


class Services(mixins.BreadcrumbsMixin, ListView):
    model = models.Service
    template_name = 'main/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        return get_list_or_404(models.Service.objects.all())

    def get_breadcrumbs(self):
        return [{'link': '/', 'title': 'Главная'}, {'link': '/services/', 'title': 'Услуги'}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class Service(mixins.BreadcrumbsMixin, DetailView):
    template_name = 'main/service.html'
    context_object_name = 'service'
    allow_empty = False

    def get_object(self):
        if not hasattr(self, '_object'):
            self._object = get_object_or_404(models.Service.objects.all(), slug=self.kwargs['service_slug'])
        return self._object

    def get_breadcrumbs(self, service=None):
        if service is None:
            service = self.get_object()
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/services/', 'title': 'Услуги'},
            {'link': f'/services/{service.slug}', 'title': service.name},
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        context['service'] = service
        context['breadcrumbs'] = self.get_breadcrumbs(service)
        return context
