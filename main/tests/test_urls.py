from django.test import TestCase
from django.urls import reverse
from ..models import Service, Category, Product

class StaticPagesTests(TestCase):
    """Tests for static pages in the application."""
    def setUp(self):
        """
        Set up test data for static pages.
        We create the necessary objects for tests, we create a category with the title "Термочехлы", because it is loaded on the main page
        """
        self.category = Category.objects.create(id=1, title="Термочехлы", slug="test-category")
        self.product = Product.objects.create(
            title="Тестовый продукт",
            slug="test-product",
            category=self.category,
            content={
                "title": "Тестовый продукт",
                "brief_desc": "Краткое описание",
                "description": [{"type": "paragraph", "value": "Подробное описание"}],
                "tables": [],
                "images": [],
                "documents": []
            }
        )
        self.service = Service.objects.create(
            name="Тестовая услуга",
            slug="test-service",
            content=[{"type": "paragraph", "value": "Описание услуги"}]
        )

    def test_home_page(self):
        """Test the home page loads successfully."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_page(self):
        """Test the catalog page loads successfully."""
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        """Test the about page loads successfully."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_certificates_page(self):
        """Test the certificates page loads successfully."""
        response = self.client.get(reverse('certificates'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page(self):
        """Test the contacts page loads successfully."""
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_delivery_page(self):
        """Test the delivery page loads successfully."""
        response = self.client.get(reverse('delivery'))
        self.assertEqual(response.status_code, 200)

    def test_complete_projects_page(self):
        """Test the complete projects page loads successfully."""
        response = self.client.get(reverse('complete_projects'))
        self.assertEqual(response.status_code, 200)

class DynamicSlugTests(TestCase):
    """Tests for dynamic slugs in the application."""
    def setUp(self):
        """Set up test data for dynamic slug tests"""
        self.service = Service.objects.create(
            name="Монтаж",
            slug="montazh",
            content=[{"type": "paragraph", "value": "Описание услуги"}]
        )

        self.category = Category.objects.create(
            title="Чехлы",
            slug="chehly"
        )

        self.product = Product.objects.create(
            title="Чехол X",
            slug="chehol-x",
            category=self.category,
            content={
                "title": "Чехол X",
                "brief_desc": "Краткое описание",
                "description": [{"type": "paragraph", "value": "Подробное описание"}],
                "tables": [],
                "images": [],
                "documents": []
            }
        )

    def test_service_detail_page(self):
        """Test the service detail page loads successfully."""
        response = self.client.get(reverse('service', kwargs={'service_slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)

    def test_category_redirect(self):
        """Test redirect from category page to product page if only one product exists."""
        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 302)

    def test_category_detail_page(self):
        """Test the category detail page loads successfully when it has more than one product."""
        self.product2 = Product.objects.create(
            title="Чехол XX",
            slug="chehol-xx",
            category=self.category,
            content={
                "title": "Чехол XX",
                "brief_desc": "Краткое описание",
                "description": [{"type": "paragraph", "value": "Подробное описание"}],
                "tables": [],
                "images": [],
                "documents": []
            }
        )

        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page(self):
        """Test the product detail page loads successfully."""
        response = self.client.get(reverse('product', kwargs={'product_slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

class PageNotFoundTest(TestCase):
    """Tests for handling 404 page not found errors."""
    def test_404_page(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Страница не найдена", status_code=404)