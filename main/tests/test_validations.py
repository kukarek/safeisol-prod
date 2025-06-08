from django.test import TestCase
from django.core.exceptions import ValidationError
from main.models import Product, Category, CompleteProject, Service, Certificate, ContactRequest

class ContactRequestValidationTest(TestCase):
    """Tests for ContactRequest model validation."""
    def test_contact_request_name_required(self):
        """Test that name is required for ContactRequest."""
        contact = ContactRequest(
            name='',  # пустое имя
            phone='+79998887766',
            email='valid@example.com',
            comment='Test comment'
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()  # вызывает валидацию модели

        self.assertIn('name', cm.exception.message_dict)

    def test_contact_request_email_invalid(self):
        """Test that email must be valid."""
        contact = ContactRequest(
            name='Test',
            phone='+79998887766',
            email='invalid-email',
            comment='Test comment'
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()

        self.assertIn('email', cm.exception.message_dict)

    def test_contact_request_phone_required(self):
        """Test that phone is required and must be valid."""
        contact = ContactRequest(
            name='Test',
            phone='',  # пустой телефон
            email='valid@example.com',
            comment='Test comment'
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()

        self.assertIn('phone', cm.exception.message_dict)

class ProductsModelValidationTest(TestCase):
    """Tests for Products model validation."""
    def setUp(self):
        """Set up test data for Products model tests."""
        self.category = Category.objects.create(title="Категория", slug="kategory")

    def test_valid_product(self):
        """Test that a valid product passes validation."""
        product = Product(
            title="Товар 1",
            slug="product-1",
            content={"title": "Товар 1", "brief_desc": "", "description": [], "tables": [], "images": [], "documents": []},
            category=self.category
        )
        # Должен успешно пройти валидацию
        product.full_clean()

    def test_slug_too_short(self):
        """Test that slug must be at least 3 characters long."""
        product = Product(
            title="Товар 1",
            slug="a",
            content={},
            category=self.category
        )
        with self.assertRaises(ValidationError) as cm:
            product.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_slug_too_long(self):
        """Test that slug must not exceed 100 characters."""
        product = Product(
            title="Товар 1",
            slug="a"*101,
            content={},
            category=self.category
        )
        with self.assertRaises(ValidationError) as cm:
            product.full_clean()
        self.assertIn('slug', cm.exception.message_dict)


class CategoriesModelValidationTest(TestCase):
    """Tests for Categories model validation."""
    def test_valid_category(self):
        """Test that a valid category passes validation."""
        category = Category(title="Категория", slug="valid-slug")
        category.full_clean()

    def test_slug_too_short(self):
        """Test that slug must be at least 3 characters long."""
        category = Category(title="Категория", slug="a")
        with self.assertRaises(ValidationError) as cm:
            category.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_slug_too_long(self):
        """Test that slug must not exceed 100 characters."""
        category = Category(title="Категория", slug="a"*101)
        with self.assertRaises(ValidationError) as cm:
            category.full_clean()
        self.assertIn('slug', cm.exception.message_dict)


class CompleteProductsModelValidationTest(TestCase):
    """Tests for CompleteProject model validation."""
    def test_valid_complete_product(self):
        """Test that a valid complete product passes validation."""
        cp = CompleteProject(name="Завершенный продукт", image_path="path/to/image.jpg")
        cp.full_clean()

    def test_name_required(self):
        """Test that name is required for CompleteProject."""
        cp = CompleteProject(name="", image_path="path/to/image.jpg")
        with self.assertRaises(ValidationError) as cm:
            cp.full_clean()
        self.assertIn('name', cm.exception.message_dict)

    def test_image_path_required(self):
        """Test that image_path is required for CompleteProject."""
        cp = CompleteProject(name="Продукт", image_path="")
        with self.assertRaises(ValidationError) as cm:
            cp.full_clean()
        self.assertIn('image_path', cm.exception.message_dict)


class ServicesModelValidationTest(TestCase):
    """Tests for Services model validation."""
    def test_valid_service(self):
        """Test that a valid service passes validation."""
        service = Service(
            name="Услуга",
            slug="valid-slug",
            content=[{"type": "paragraph", "value": "Описание"}]
        )
        service.full_clean()

    def test_slug_too_short(self):
        """Test that slug must be at least 5 characters long."""
        service = Service(name="Услуга", slug="a", content=[])
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_slug_too_long(self):
        """Test that slug must not exceed 100 characters."""
        service = Service(name="Услуга", slug="a"*101, content=[])
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_name_required(self):
        """Test that name is required for Services."""
        service = Service(name="", slug="valid-slug", content=[])
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('name', cm.exception.message_dict)

    def test_content_required(self):
        """Test that content is required for Services."""
        service = Service(name="Услуга", slug="valid-slug", content=None)
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('content', cm.exception.message_dict)


class CertificatesModelValidationTest(TestCase):
    """Tests for Certificates model validation."""
    def test_valid_certificate(self):
        """Test that a valid certificate passes validation."""
        cert = Certificate(title="Сертификат")
        cert.full_clean()

    def test_title_required(self):
        """Test that title is required for Certificates."""
        cert = Certificate(title="")
        with self.assertRaises(ValidationError) as cm:
            cert.full_clean()
        self.assertIn('title', cm.exception.message_dict)