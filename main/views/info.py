from django.views.generic import TemplateView
from main import models, mixins
from django.core.paginator import Paginator

class About(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "About Us" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/about.html'
    section = 'about'
    subtitle = 'О компании'


    def get_breadcrumbs(self):
        return [
            {"title": "Главная", "url": "/"},
            {"title": self.subtitle, "url": ""},
        ]


class Certificates(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "Certificates" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/certificates.html'
    section = 'certificates'
    subtitle = 'Сертификаты'

    def get_breadcrumbs(self):
        return [
            {"title": "Главная", "url": "/"},
            {"title": "О компании", "url": "/about/"},
            {"title": self.subtitle, "url": ""},
        ]
    

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


    def get_breadcrumbs(self):
        return [
            {"title": "Главная", "url": "/"},
            {"title": self.subtitle, "url": ""},
        ]


class Delivery(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    """
    View for the "Delivery" page.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation and SectionMixin for section handling.
    """
    template_name = 'main/delivery.html'
    section = 'delivery'
    subtitle = 'Доставка'


    def get_breadcrumbs(self):
        return [
            {"title": "Главная", "url": "/"},
            {"title": self.subtitle, "url": ""},
        ]


class CompleteProjects(mixins.BreadcrumbsMixin, mixins.SectionMixin, TemplateView):
    template_name = 'main/complete_projects.html'
    section = 'complete_projects'
    subtitle = 'Выполненные проекты'
    paginate_by = 8


    def get_breadcrumbs(self):
        return [
            {"title": "Главная", "url": "/"},
            {"title": self.subtitle, "url": ""},
        ]
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_projects = models.CompleteProject.objects.all()
        paginator = Paginator(all_projects, self.paginate_by)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['products'] = page_obj.object_list
        return context
