from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from main import models


class Index(TemplateView):
    """
    View for the main page of the application.
    This view renders the 'main.html' template and provides context data for the page.
    The context includes the main category "Термочехлы" and a virtual category with other products.
    """
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs) -> dict:
        """
        Returns the context data for the main page.
        This method adds the main category "Термочехлы" and a virtual category with other products to the context.
        It retrieves the "Термочехлы" category from the database and excludes its products from the virtual category.
        If the "Термочехлы" category does not exist, it raises a 404 error.
        """
        context = super().get_context_data(**kwargs)

        # Получаем категорию "Термочехлы"
        cat_termochehly = get_object_or_404(models.Category, title='Термочехлы')

        # Виртуальная категория с остальными продуктами
        temp_category = {
            'title': 'Дополнительно',
            'slug': 'temp-category',
            'get_absolute_url': reverse('catalog'),
            'products': models.Product.objects.exclude(category_id=cat_termochehly.id)
        }

        context['categories'] = [cat_termochehly, temp_category]
        context['additional_category'] = temp_category

        return context
