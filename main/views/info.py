from django.views.generic import TemplateView
from django.http import Http404
from main import models, mixins


class About(mixins.BreadcrumbsMixin, TemplateView):
    """
    View for the "About" page of the application.
    This view inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    It renders the 'about.html' template and provides context data for the page.
    The context includes the section identifier and subtitle for the page.
    """
    template_name = 'main/about.html'

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the "About" page.
        The breadcrumbs include links to the home page and the "About" page.
        """
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/about/', 'title': 'О компании'}
        ]

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the "About" page.
        This method adds the section identifier and subtitle to the context.
        It also retrieves the content for the "About" page from the database.
        If the content is not found, it raises a 404 error.
        """
        context = super().get_context_data(**kwargs)
        context['section'] = 'about'
        context['subtitle'] = 'О компании'
        return context
    
class Certificates(mixins.BreadcrumbsMixin, TemplateView):
    """
    View for the "Certificates" page of the application.
    This view inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    It renders the 'certificates.html' template and provides context data for the page.
    The context includes the section identifier, subtitle, and a list of certificate titles.
    """
    template_name = 'main/certificates.html'

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the "Certificates" page.
        The breadcrumbs include links to the home page, "About" page, and the "Certificates" page.
        """
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/about/', 'title': 'О компании'},
            {'link': '/about/certificates/', 'title': 'Сертификаты'}
        ]

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the "Certificates" page.
        This method adds the section identifier, subtitle, and a list of certificate titles to the context.
        It retrieves the titles of all certificates from the database.
        If no certificates are found, it returns an empty list.
        """
        context = super().get_context_data(**kwargs)
        context['section'] = 'certificates'
        context['subtitle'] = 'Сертификаты'
        context['certificates'] = list(models.Certificate.objects.values_list('title', flat=True))
        return context

class Contacts(mixins.BreadcrumbsMixin, TemplateView):
    """
    View for the "Contacts" page of the application.
    This view inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    It renders the 'contacts.html' template and provides context data for the page.
    The context includes the section identifier and subtitle for the page.
    """
    template_name = 'main/contacts.html'

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the "Contacts" page.
        The breadcrumbs include links to the home page and the "Contacts" page.
        """
        return [{'link': '/', 'title': 'Главная'}, {'link': '/contacts/', 'title': 'Контакты'}]


class Delivery(mixins.BreadcrumbsMixin, TemplateView):
    """
    View for the "Delivery" page of the application.
    This view inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    It renders the 'delivery.html' template and provides context data for the page.
    The context includes the section identifier and subtitle for the page.
    """
    template_name = 'main/delivery.html'

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the "Delivery" page.
        The breadcrumbs include links to the home page and the "Delivery" page.
        """
        return [{'link': '/', 'title': 'Главная'}, {'link': '/delivery/', 'title': 'Доставка'}]


class CompleteProjects(mixins.BreadcrumbsMixin, TemplateView):
    """
    View for the "Complete Projects" page of the application.
    This view inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    It renders the 'complete_projects.html' template and provides context data for the page.
    The context includes a list of completed projects.
    """
    template_name = 'main/complete_projects.html'

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the "Complete Projects" page.
        The breadcrumbs include links to the home page and the "Complete Projects" page.
        """
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/complete_projects/', 'title': 'Выполненные проекты'}
        ]

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the "Complete Projects" page.
        This method adds a list of all completed projects to the context.
        If no completed projects are found, it returns an empty list.
        """
        context = super().get_context_data(**kwargs)
        context['products'] = models.CompleteProject.objects.all()
        return context

