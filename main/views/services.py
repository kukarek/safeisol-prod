from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, get_list_or_404
from main import models, mixins



class Services(mixins.BreadcrumbsMixin, ListView):
    model = models.Services
    template_name = 'main/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        return get_list_or_404(models.Services)

    def get_breadcrumbs(self):
        return [{'link': '/', 'title': 'Главная'}, {'link': '/services/', 'title': 'Услуги'}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()  # Используем метод get_breadcrumbs из миксина
        return context


class Service(mixins.BreadcrumbsMixin, DetailView):
    template_name = 'main/service.html'
    context_object_name = 'service'
    allow_empty = False

    def get_object(self):
        return get_object_or_404(models.Services.objects, slug=self.kwargs['service_slug'])

    def get_breadcrumbs(self):
        service = self.get_object()
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/services/', 'title': 'Услуги'},
            {'link': f'/services/{service.slug}', 'title': service.name}
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.get_object()
        context['breadcrumbs'] = self.get_breadcrumbs()  # Используем метод get_breadcrumbs из миксина
        return context
