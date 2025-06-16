from django.contrib.sitemaps import Sitemap
import inspect
from django.urls import reverse
from django.db.models.query import QuerySet
from .models import Product, Category


class SitemapRegistry:
    """
    Registry for managing sitemap classes.
    This class allows for the registration of sitemap classes and provides
    a method to retrieve all registered sitemaps.
    Attributes:
        _registry (dict): A dictionary to hold registered sitemap instances.
    """
    _registry = {}

    @classmethod
    def register(cls, sitemap_cls) -> 'Sitemap':
        """
        Registers a sitemap class in the registry.
        This method takes a sitemap class as an argument, creates an instance of it,
        and adds it to the registry with a key derived from the class name.
        Args:
            sitemap_cls (Sitemap): The sitemap class to register.
        Returns:
            Sitemap: An instance of the registered sitemap class.
        """
        key = sitemap_cls.__name__.replace('Sitemap', '').lower()
        cls._registry[key] = sitemap_cls()
        return sitemap_cls

    @classmethod
    def get_sitemaps(cls) -> dict:
        """
        Returns all registered sitemaps.
        This method retrieves all sitemap instances from the registry.
        Returns:
            dict: A dictionary containing all registered sitemap instances.
        """
        return cls._registry
    
    
@SitemapRegistry.register
class ProductSitemap(Sitemap):
    """
    Sitemap for products in the catalog.
    This class generates a sitemap for all products, allowing search engines
    to discover and index them efficiently.
    Attributes:
        changefreq (str): How frequently the product pages are likely to change.
        priority (float): The priority of the product pages relative to other pages.
    """
    changefreq = "weekly"
    priority = 0.9

    def items(self) -> 'QuerySet[Product]':
        """
        Returns a queryset of all products to be included in the sitemap.
        This method retrieves all products from the database.
        Returns:
            QuerySet: A queryset containing all Product objects.
        """
        return Product.objects.all()

    def location(self, obj: Product) -> str:
        """
        Returns the URL for a given product object.
        This method generates the absolute URL for each product based on its slug.
        Args:
            obj (Product): The product object for which to generate the URL.
        Returns:
            str: The absolute URL of the product.
        """
        return obj.get_absolute_url()

@SitemapRegistry.register
class CategorySitemap(Sitemap):
    """
    Sitemap for product categories.
    This class generates a sitemap for all product categories, allowing search engines
    to discover and index them efficiently.
    Attributes:
        changefreq (str): How frequently the category pages are likely to change.
        priority (float): The priority of the category pages relative to other pages.
    """
    changefreq = "weekly"
    priority = 0.7


    def items(self) -> 'QuerySet[Category]':
        """
        Returns a queryset of all categories to be included in the sitemap.
        This method retrieves all categories from the database.
        Returns:
            QuerySet: A queryset containing all Category objects.
        """
        return Category.objects.all()


    def location(self, obj: Category) -> str:
        """
        Returns the URL for a given category object.
        This method generates the absolute URL for each category based on its slug.
        Args:
            obj (Category): The category object for which to generate the URL.
        """
        return obj.get_absolute_url()

@SitemapRegistry.register
class StaticViewSitemap(Sitemap):
    """
    Sitemap for static views of the site.
    This class generates a sitemap for static pages such as home, catalog, about,
    certificates, contacts, delivery, complete projects, and services.
    Attributes:
        changefreq (str): How frequently the static pages are likely to change.
        priority (float): The priority of the static pages relative to other pages.
    """
    changefreq = "monthly"
    priority = 0.5


    def items(self) -> list:
        """
        Returns a list of static view names to be included in the sitemap.
        This method defines the static pages that should be indexed by search engines.
        Returns:
            list: A list of static view names.
        """
        return [
            "home", "catalog", "about", "certificates",
            "contacts", "delivery", "complete_projects", "services"
        ]


    def location(self, item) -> str:
        """
        Returns the URL for a given static view name.
        This method generates the absolute URL for each static view based on its name.
        Args:
            item (str): The name of the static view for which to generate the URL.
        """
        return reverse(item)
