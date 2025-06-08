from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, get_list_or_404
from main import models, mixins

class Services(mixins.BreadcrumbsMixin, ListView):
    """
    View for displaying a list of services.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    """
    model = models.Service
    template_name = 'main/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        """
        Returns a list of all services.
        Uses get_list_or_404 to return a 404 error if no services are found.
        """
        return get_list_or_404(models.Service)

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the services page.
        The breadcrumbs include links to the home page and the services page.
        """
        return [{'link': '/', 'title': 'Главная'}, {'link': '/services/', 'title': 'Услуги'}]

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the services page.
        Adds the list of services and breadcrumbs to the context.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()  
        return context


class Service(mixins.BreadcrumbsMixin, DetailView):
    """
    View for displaying a specific service.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    """
    template_name = 'main/service.html'
    context_object_name = 'service'
    allow_empty = False

    def get_object(self):
        """
        Returns the service object based on the slug provided in the URL.
        Uses get_object_or_404 to return a 404 error if the service does not exist.
        """
        return get_object_or_404(models.Service.objects, slug=self.kwargs['service_slug'])

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the service detail page.
        The breadcrumbs include links to the home page, services page, and the specific service.
        """
        service = self.get_object()
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/services/', 'title': 'Услуги'},
            {'link': f'/services/{service.slug}', 'title': service.name}
        ]

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the service detail page.
        Adds the service object and breadcrumbs to the context.
        """
        context = super().get_context_data(**kwargs)
        context['service'] = self.get_object()
        context['breadcrumbs'] = self.get_breadcrumbs()  
        return context
