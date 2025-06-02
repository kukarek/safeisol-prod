from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404, redirect
from main import models, mixins


class Catalog(mixins.BreadcrumbsMixin, TemplateView):
    template_name = 'main/catalog.html'

    def get_breadcrumbs(self):
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/catalog/', 'title': 'Каталог'}
        ]

    def get_objects(self, queryset=None):
        return models.Categories.objects.all().prefetch_related('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_objects()
        return context


class Category(mixins.BreadcrumbsMixin, DetailView):
    model = models.Categories
    template_name = 'main/category.html'
    context_object_name = 'categories_dict'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Categories.objects.prefetch_related('products'), slug=self.kwargs['category_slug'])

    def get_breadcrumbs(self):
        category = self.get_object()
        breadcrumbs = [
            {'link': '/', 'title': 'Главная'},
            {'link': '/catalog/', 'title': 'Каталог'},
            {'link': f'/category/{category.slug}', 'title': category.title}
        ]
        return breadcrumbs

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        if category.products.count() == 1:
            product = category.products.first()
            return redirect('product', product_slug=product.slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['categories'] = [category]
        return context



class Product(mixins.BreadcrumbsMixin, DetailView):
    template_name = 'main/product.html'
    context_object_name = 'product'
    allow_empty = False

    def get_object(self):
        return get_object_or_404(models.Products.objects.prefetch_related('category'), slug=self.kwargs['product_slug'])

    def get_breadcrumbs(self):
        product = self.get_object()
        breadcrumbs = [
            {'link': '/', 'title': 'Главная'},
            {'link': '/catalog/', 'title': 'Каталог'}
        ]
        if models.Products.objects.filter(category=product.category).count() > 1:
            breadcrumbs.append({'link': f'/category/{product.category.slug}', 'title': product.category.title})
        breadcrumbs.append({'link': f'/product/{product.slug}', 'title': product.title})
        return breadcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['product'] = product
        return context