from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404, redirect
from main import models, mixins


class Catalog(mixins.BreadcrumbsMixin, TemplateView):
    """
    View for displaying the catalog of categories and their products.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    """
    template_name = 'main/catalog.html'

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the catalog page.
        The breadcrumbs include links to the home page and the catalog page.
        """
        return [
            {'link': '/', 'title': 'Главная'},
            {'link': '/catalog/', 'title': 'Каталог'}
        ]

    def get_objects(self, queryset=None):
        """
        Returns all categories with their related products.
        Uses prefetch_related to optimize database queries.
        """
        return models.Category.objects.all().prefetch_related('products')

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the catalog page.
        Adds the list of categories to the context.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_objects()
        return context


class Category(mixins.BreadcrumbsMixin, DetailView):
    """
    View for displaying a specific category and its products.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    """
    model = models.Category
    template_name = 'main/category.html'
    context_object_name = 'categories_dict'

    def get_object(self, queryset=None):
        """
        Returns the category object based on the slug provided in the URL.
        Uses get_object_or_404 to return a 404 error if the category does not exist.
        Prefetches related products to optimize database queries.
        """
        return get_object_or_404(models.Category.objects.prefetch_related('products'), slug=self.kwargs['category_slug'])

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the category page.
        The breadcrumbs include links to the home page, catalog page, and the specific category.
        """
        category = self.get_object()
        breadcrumbs = [
            {'link': '/', 'title': 'Главная'},
            {'link': '/catalog/', 'title': 'Каталог'},
            {'link': f'/category/{category.slug}', 'title': category.title}
        ]
        return breadcrumbs

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the category view.
        If the category has only one product, redirects to the product detail page.
        Otherwise, renders the category page with the list of products.
        """
        category = self.get_object()
        if category.products.count() == 1:
            product = category.products.first()
            return redirect('product', product_slug=product.slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the category page.
        Adds the category object to the context.
        """
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['categories'] = [category]
        return context



class Product(mixins.BreadcrumbsMixin, DetailView):
    """
    View for displaying a specific product.
    Inherits from BreadcrumbsMixin to provide breadcrumb navigation.
    """
    template_name = 'main/product.html'
    context_object_name = 'product'
    allow_empty = False

    def get_object(self):
        """
        Returns the product object based on the slug provided in the URL.
        Uses get_object_or_404 to return a 404 error if the product does not exist.
        Prefetches related category to optimize database queries.
        """
        return get_object_or_404(models.Product.objects.prefetch_related('category'), slug=self.kwargs['product_slug'])

    def get_breadcrumbs(self):
        """
        Returns a list of breadcrumbs for the product page.
        The breadcrumbs include links to the home page, catalog page, category page (if applicable), and the specific product.
        """
        product = self.get_object()
        breadcrumbs = [
            {'link': '/', 'title': 'Главная'},
            {'link': '/catalog/', 'title': 'Каталог'}
        ]
        if models.Product.objects.filter(category=product.category).count() > 1:
            breadcrumbs.append({'link': f'/category/{product.category.slug}', 'title': product.category.title})
        breadcrumbs.append({'link': f'/product/{product.slug}', 'title': product.title})
        return breadcrumbs

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the product page.
        Adds the product object to the context.
        """
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['product'] = product
        return context