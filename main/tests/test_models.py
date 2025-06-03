from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from ..models import Products, Categories, Services, Certificates, ContactRequest
from unittest.mock import patch

class CategoriesModelTest(TestCase):
    def test_category_creation(self):
        category = Categories.objects.create(title="Категория A", slug="kategoria-a")
        self.assertEqual(str(category), "Категория A")
        self.assertEqual(category.get_absolute_url(), reverse('category', kwargs={'category_slug': category.slug}))

    def test_category_slug_validation(self):
        category = Categories(title="Тест", slug="abc")  # < 5 символов
        with self.assertRaises(ValidationError):
            category.full_clean()

class ProductsModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(title="Категория B", slug="category-b")

    def test_product_creation_and_url(self):
        content = {
            "title": "Продукт X",
            "brief_desc": "Кратко",
            "description": [{"type": "paragraph", "value": "Описание"}],
            "tables": [],
            "images": [],
            "documents": []
        }

        product = Products.objects.create(
            title="Продукт X",
            slug="product-x",
            category=self.category,
            content=content
        )

        self.assertEqual(str(product), "Продукт X")
        self.assertEqual(product.get_absolute_url(), reverse('product', kwargs={'product_slug': product.slug}))
        self.assertEqual(product.category, self.category)
        self.assertIn("brief_desc", product.content)

    def test_product_slug_validation(self):
        product = Products(
            title="Неверный",
            slug="a",  # слишком короткий
            content={},
            category=self.category
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

class ServicesModelTest(TestCase):
    def test_services_str_and_slug_validation(self):
        content = [{"type": "paragraph", "value": "Текст"}]
        service = Services(name="Монтаж", slug="montazh", content=content)
        service.full_clean()  # slug valid
        service.save()
        self.assertEqual(service.name, "Монтаж")
        self.assertEqual(service.slug, "montazh")

        invalid_service = Services(name="Некоррект", slug="ab", content=content)  # короткий slug
        with self.assertRaises(ValidationError):
            invalid_service.full_clean()

class CertificatesModelTest(TestCase):
    def test_certificate_str(self):
        certificate = Certificates.objects.create(title="Сертификат 1")
        self.assertEqual(str(certificate), "Сертификат 1")

class ContactRequestModelTest(TestCase):

    @patch('main.signals.send_notification_email.delay')
    def test_signal_triggers_on_contact_creation(self, mock_delay):
        contact = ContactRequest.objects.create(
            name="Test",
            phone="+79998887766",
            email="test@test.com",
            comment="Test"
        )
        # Проверка строки
        self.assertEqual(str(contact), "Test (test@test.com)")

        # Проверка дефолтного статуса
        self.assertEqual(contact.status, "pending")
        self.assertEqual(contact.error_message, "")

        # Проверка, что задача отправки письма была вызвана
        mock_delay.assert_called_once_with(contact.pk)

