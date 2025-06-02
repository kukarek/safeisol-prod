from django.views.generic import TemplateView
from django.http import Http404
from main import models, mixins


class About(mixins.BreadcrumbsMixin, TemplateView):
    template_name = 'main/about.html'

    def get_breadcrumbs(self):
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/about/', 'title': 'О компании'}
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'about'
        context['subtitle'] = 'О компании'
        return context
    
class Certificates(mixins.BreadcrumbsMixin, TemplateView):
    template_name = 'main/certificates.html'

    def get_breadcrumbs(self):
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/about/', 'title': 'О компании'},
            {'link': '/about/certificates/', 'title': 'Сертификаты'}
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'certificates'
        context['subtitle'] = 'Сертификаты'
        context['certificates'] = list(models.Certificates.objects.values_list('title', flat=True))
        return context

class Contacts(mixins.BreadcrumbsMixin, TemplateView):
    template_name = 'main/contacts.html'

    def get_breadcrumbs(self):
        return [{'link': '/', 'title': 'Главная'}, {'link': '/contacts/', 'title': 'Контакты'}]


class Delivery(mixins.BreadcrumbsMixin, TemplateView):
    template_name = 'main/delivery.html'

    def get_breadcrumbs(self):
        return [{'link': '/', 'title': 'Главная'}, {'link': '/delivery/', 'title': 'Доставка'}]


class CompleteProjects(mixins.BreadcrumbsMixin, TemplateView):
    template_name = 'main/complete_projects.html'

    def get_breadcrumbs(self):
        return [{'link': '/', 'title': 'Главная'}, {'link': '/complete_projects/', 'title': 'Выполненные проекты'}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = range(37)
        return context

