from django.test import TestCase
from django.urls import reverse
from ..models import Services, Categories, Products

class StaticPagesTests(TestCase):

    def setUp(self):
        # Создаем необходимые объекты для тестов, категорию создаем с тайтлом Термочехлы, потому-что она загружается на главной странице
        self.category = Categories.objects.create(id=1, title="Термочехлы", slug="test-category")
        self.product = Products.objects.create(
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
        self.service = Services.objects.create(
            name="Тестовая услуга",
            slug="test-service",
            content=[{"type": "paragraph", "value": "Описание услуги"}]
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_page(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_certificates_page(self):
        response = self.client.get(reverse('certificates'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_delivery_page(self):
        response = self.client.get(reverse('delivery'))
        self.assertEqual(response.status_code, 200)

    def test_complete_projects_page(self):
        response = self.client.get(reverse('complete_projects'))
        self.assertEqual(response.status_code, 200)

class DynamicSlugTests(TestCase):
    
    def setUp(self):
        self.service = Services.objects.create(
            name="Монтаж",
            slug="montazh",
            content=[{"type": "paragraph", "value": "Описание услуги"}]
        )

        self.category = Categories.objects.create(
            title="Чехлы",
            slug="chehly"
        )

        self.product = Products.objects.create(
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
        response = self.client.get(reverse('service', kwargs={'service_slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)

    def test_category_redirect(self):

        #Если в категории только один товар, то редирект на страницу товара
        response = self.client.get(reverse('category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 302)

    def test_category_detail_page(self):
        
        #Страница категории показываеться только если в ней больше одного товара иначе редирект на страницу товара
        self.product2 = Products.objects.create(
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
        response = self.client.get(reverse('product', kwargs={'product_slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

class PageNotFoundTest(TestCase):
    def test_404_page(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Страница не найдена", status_code=404)