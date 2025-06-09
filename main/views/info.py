from django.views.generic import TemplateView
from main import models, mixins

class About(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "About Us" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/about.html'
    section = 'about'
    subtitle = 'О компании'


class Certificates(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "Certificates" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/certificates.html'
    section = 'certificates'
    subtitle = 'Сертификаты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # лучше возвращать объекты, а не только заголовки
        context['certificates'] = models.Certificate.objects.all()
        return context


class Contacts(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "Contacts" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/contacts.html'
    section = 'contacts'
    subtitle = 'Контакты'


class Delivery(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "Delivery" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/delivery.html'
    section = 'delivery'
    subtitle = 'Доставка'


class CompleteProjects(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "Complete Projects" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/complete_projects.html'
    section = 'complete_projects'
    subtitle = 'Выполненные проекты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = models.CompleteProject.objects.all()
        return context
