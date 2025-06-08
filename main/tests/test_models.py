from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from ..models import Product, Category, Service, Certificate, ContactRequest, CompleteProject
from unittest.mock import patch

class CategoriesModelTest(TestCase):
    """Tests for Categories model."""
    def test_category_creation(self):
        """Test creating a category and its string representation."""
        category = Category.objects.create(title="Категория A", slug="kategoria-a")
        self.assertEqual(str(category), "Категория A")
        self.assertEqual(category.get_absolute_url(), reverse('category', kwargs={'category_slug': category.slug}))

    def test_category_slug_validation(self):
        """Test slug validation for Categories model."""
        category = Category(title="Тест", slug="abc")  # < 5 символов
        with self.assertRaises(ValidationError):
            category.full_clean()

class ProductsModelTest(TestCase):
    """Tests for Products model."""
    def setUp(self):
        """Set up test data for Products model tests."""
        self.category = Category.objects.create(title="Категория B", slug="category-b")

    def test_product_creation_and_url(self):
        """Test creating a product and its string representation and URL."""
        content = {
            "title": "Продукт X",
            "brief_desc": "Кратко",
            "description": [{"type": "paragraph", "value": "Описание"}],
            "tables": [],
            "images": [],
            "documents": []
        }

        product = Product.objects.create(
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
        """Test slug validation for Products model."""
        product = Product(
            title="Неверный",
            slug="a",  # слишком короткий
            content={},
            category=self.category
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

class ServicesModelTest(TestCase):
    """Tests for Services model."""
    def test_services_str_and_slug_validation(self):
        """Test string representation and slug validation for Services model."""
        content = [{"type": "paragraph", "value": "Текст"}]
        service = Service(name="Монтаж", slug="montazh", content=content)
        service.full_clean()  # slug valid
        service.save()
        self.assertEqual(service.name, "Монтаж")
        self.assertEqual(service.slug, "montazh")

        invalid_service = Service(name="Некоррект", slug="ab", content=content)  
        with self.assertRaises(ValidationError):
            invalid_service.full_clean()

class CertificatesModelTest(TestCase):
    """Tests for Certificates model."""
    def test_certificate_str(self):
        """Test string representation of Certificates model."""
        certificate = Certificate.objects.create(title="Сертификат 1")
        self.assertEqual(str(certificate), "Сертификат 1")

class ContactRequestModelTest(TestCase):
    """Tests for ContactRequest model."""
    @patch('main.signals.send_notification_email.delay')
    def test_signal_triggers_on_contact_creation(self, mock_delay):
        """Test that the signal triggers email sending on contact creation."""
        contact = ContactRequest.objects.create(
            name="Test",
            phone="+79998887766",
            email="test@test.com",
            comment="Test"
        )
        
        self.assertEqual(str(contact), "Test (test@test.com)")
        self.assertEqual(contact.status, "pending")
        self.assertEqual(contact.error_message, "")
        # Проверяем, что задача отправки письма была вызвана
        mock_delay.assert_called_once_with(contact.pk)

class CompleteProjectModelTest(TestCase):
    """Tests for CompleteProject model."""
    def test_complete_project_creation(self):
        """Test creating a complete project and its string representation."""
        project = CompleteProject.objects.create(
            name="Завершенный проект",
            image_path="zavershennyi-proekt.png",
        )
        self.assertEqual(str(project), "Завершенный проект")

