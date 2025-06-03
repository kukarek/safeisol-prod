from django.test import TestCase
from django.urls import reverse
from main.models import Categories, Products, Services, Certificates


class CatalogViewTest(TestCase):
    def test_catalog_page(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(title="Чехлы", slug="chehly")

    def test_redirect_if_one_product(self):
        product = Products.objects.create(title="Продукт 1", slug="product-1", content={}, category=self.category)
        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertRedirects(response, reverse('product', kwargs={'product_slug': product.slug}))

    def test_show_category_with_multiple_products(self):
        Products.objects.create(title="Продукт 1", slug="product-1", content={}, category=self.category)
        Products.objects.create(title="Продукт 2", slug="product-2", content={}, category=self.category)
        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)


class ProductViewTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(title="Чехлы", slug="chehly")
        self.product = Products.objects.create(title="Продукт", slug="product", content={}, category=self.category)

    def test_product_view(self):
        response = self.client.get(reverse('product', kwargs={'product_slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)

class IndexViewTest(TestCase):

    def setUp(self):
        self.cat1 = Categories.objects.create(id=1, title="Термочехлы", slug="termochehly")
        self.cat2 = Categories.objects.create(id=2, title="Чехлы", slug="chehly")
        
        self.product1 = Products.objects.create(
            slug="product-1", title="Product 1", content={}, category=self.cat1
        )
        self.product2 = Products.objects.create(
            slug="product-2", title="Product 2", content={}, category=self.cat2
        )

    def test_index_view_context(self):
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
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'main/main.html')

class StaticPagesTest(TestCase):
    
    def setUp(self):
        Certificates.objects.create(title="Сертификат ISO 9001")

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertEqual(response.context['section'], 'about')
        self.assertEqual(response.context['subtitle'], 'О компании')

    def test_certificates_page(self):
        response = self.client.get(reverse('certificates'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/certificates.html')
        self.assertEqual(response.context['section'], 'certificates')
        self.assertEqual(response.context['subtitle'], 'Сертификаты')
        self.assertIn("Сертификат ISO 9001", response.context['certificates'])

    def test_contacts_page(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contacts.html')

    def test_delivery_page(self):
        response = self.client.get(reverse('delivery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delivery.html')

    def test_complete_projects_page(self):
        response = self.client.get(reverse('complete_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/complete_projects.html')
        self.assertEqual(list(response.context['products']), list(range(37)))

class ServicesViewsTest(TestCase):

    def setUp(self):
        self.service = Services.objects.create(
            name="Монтаж",
            slug="montazh",
            content=[{"type": "paragraph", "value": "Описание монтажа"}]
        )

    def test_services_list_view(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/services.html')
        self.assertIn(self.service, response.context['services'])
        self.assertIn('breadcrumbs', response.context)

    def test_service_detail_view(self):
        response = self.client.get(reverse('service', kwargs={'service_slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/service.html')
        self.assertEqual(response.context['service'], self.service)
        self.assertIn('breadcrumbs', response.context)

    def test_service_detail_404(self):
        response = self.client.get(reverse('service', kwargs={'service_slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)
