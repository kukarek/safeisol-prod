from django.test import TestCase
from django.urls import reverse
from main.models import Category, Product, Service, Certificate, CompleteProject


class CatalogViewTest(TestCase):
    """Tests for the catalog view."""
    def test_catalog_page(self):
        """Test that the catalog page loads successfully and contains categories."""
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)


class CategoryViewTest(TestCase):
    """Tests for the category view."""
    def setUp(self):
        """Set up test data for category view tests."""
        self.category = Category.objects.create(title="Чехлы", slug="chehly")

    def test_redirect_if_one_product(self):
        """Test that if there is only one product in the category, it redirects to the product page."""
        product = Product.objects.create(title="Продукт 1", slug="product-1", content={}, category=self.category)
        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertRedirects(response, reverse('product', kwargs={'product_slug': product.slug}))

    def test_show_category_with_multiple_products(self):
        """Test that the category page shows multiple products."""
        Product.objects.create(title="Продукт 1", slug="product-1", content={}, category=self.category)
        Product.objects.create(title="Продукт 2", slug="product-2", content={}, category=self.category)
        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)


class ProductViewTest(TestCase):
    """Tests for the product view."""
    def setUp(self):
        """Set up test data for product view tests."""
        self.category = Category.objects.create(title="Чехлы", slug="chehly")
        self.product = Product.objects.create(title="Продукт", slug="product", content={}, category=self.category)

    def test_product_view(self):
        """Test that the product page loads successfully and contains the product."""
        response = self.client.get(reverse('product', kwargs={'product_slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)

class IndexViewTest(TestCase):
    """Tests for the index view."""
    def setUp(self):
        """Set up test data for index view tests."""
        self.cat1 = Category.objects.create(id=1, title="Термочехлы", slug="termochehly")
        self.cat2 = Category.objects.create(id=2, title="Чехлы", slug="chehly")
        
        self.product1 = Product.objects.create(
            slug="product-1", title="Product 1", content={}, category=self.cat1
        )
        self.product2 = Product.objects.create(
            slug="product-2", title="Product 2", content={}, category=self.cat2
        )

    def test_index_view_context(self):
        """Test that the index view context contains categories and products."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        categories = response.context['categories']
        self.assertEqual(len(categories), 2)

        # Первая категория — id=1
        self.assertEqual(categories[0].id, 1)

        # Временная категория
        temp_cat = categories[1]
        self.assertEqual(temp_cat['title'], 'Дополнительно')
        self.assertIn(self.product2, temp_cat['products'])
        self.assertNotIn(self.product1, temp_cat['products'])

    def test_template_used(self):
        """Test that the index view uses the correct template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'main/main.html')

class StaticPagesTest(TestCase):
    """Tests for static pages like About, Certificates, Contacts, Delivery, and Complete Projects."""
    def setUp(self):
        """Set up test data for static pages."""
        Certificate.objects.create(title="Сертификат ISO 9001")

    def test_about_page(self):
        """Test that the about page loads successfully and contains the correct context."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertEqual(response.context['section'], 'about')
        self.assertEqual(response.context['subtitle'], 'О компании')

    def test_certificates_page(self):
        """Test that the certificates page loads successfully and contains the correct context."""
        response = self.client.get(reverse('certificates'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/certificates.html')
        self.assertEqual(response.context['section'], 'certificates')
        self.assertEqual(response.context['subtitle'], 'Сертификаты')
        self.assertIn("Сертификат ISO 9001", response.context['certificates'])

    def test_contacts_page(self):
        """Test that the contacts page loads successfully and contains the correct context."""
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contacts.html')

    def test_delivery_page(self):
        """Test that the delivery page loads successfully and contains the correct context."""
        response = self.client.get(reverse('delivery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delivery.html')

    def test_complete_projects_page(self):
        """Test that the complete projects page loads successfully and contains the correct context."""
        response = self.client.get(reverse('complete_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/complete_projects.html')
        expected_products = list(CompleteProject.objects.all())
        context_products = list(response.context['products'])
        self.assertEqual(context_products, expected_products)

class ServicesViewsTest(TestCase):
    """Tests for the services views."""
    def setUp(self):
        """Set up test data for services views."""
        self.service = Service.objects.create(
            name="Монтаж",
            slug="montazh",
            content=[{"type": "paragraph", "value": "Описание монтажа"}]
        )

    def test_services_list_view(self):
        """Test that the services list view loads successfully and contains the service."""
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/services.html')
        self.assertIn(self.service, response.context['services'])
        self.assertIn('breadcrumbs', response.context)

    def test_service_detail_view(self):
        """Test that the service detail view loads successfully and contains the service."""
        response = self.client.get(reverse('service', kwargs={'service_slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/service.html')
        self.assertEqual(response.context['service'], self.service)
        self.assertIn('breadcrumbs', response.context)

    def test_service_detail_404(self):
        """Test that accessing a non-existent service returns 404."""
        response = self.client.get(reverse('service', kwargs={'service_slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)
