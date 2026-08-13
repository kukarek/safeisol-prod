from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from main.models import Category, Product


class Index(TemplateView):
    """
    Представление для главной страницы приложения.
    Отображает шаблон 'main/main.html' и передает категории со связанными продуктами.
    """
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        # Оптимизируем выборку:
        # 1. prefetch_related загружает продукты отдельным оптимизированным запросом
        # 2. only() / select_related при необходимости помогает вытащить только нужные поля
        context['categories'] = Category.objects.prefetch_related(
            'products'
        ).all()

        return context