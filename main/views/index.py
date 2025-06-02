from django.shortcuts import render
from django.views.generic import TemplateView
from main import models


class Index(TemplateView):

    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_termochehly = models.Categories.objects.get(id=1)
        temp_category = {'title': 'Дополнительно', 'slug': 'temp-category', 'get_absolute_url': 'catalog/'}
        temp_category['products'] = models.Products.objects.exclude(category_id=1)
        context['categories'] = [cat_termochehly, temp_category]
        return context