from django.shortcuts import render
from django.views.generic import TemplateView
from main import models


class Index(TemplateView):
    """
    View for the main page of the application.
    This view inherits from TemplateView and renders the main.html template.
    It also provides context data for the categories displayed on the main page.
    The main page includes a special category for "Термочехлы" and a temporary category
    that includes all products except those in the "Термочехлы" category.
    """
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the main page.
        This method retrieves the "Термочехлы" category and creates a temporary category
        that includes all products except those in the "Термочехлы" category.
        It then adds these categories to the context under the key 'categories'.
        """
        context = super().get_context_data(**kwargs)
        cat_termochehly = models.Category.objects.get(title='Термочехлы')
        temp_category = {'title': 'Дополнительно', 'slug': 'temp-category', 'get_absolute_url': 'catalog/'}
        temp_category['products'] = models.Product.objects.exclude(category_id=1)
        context['categories'] = [cat_termochehly, temp_category]
        return context