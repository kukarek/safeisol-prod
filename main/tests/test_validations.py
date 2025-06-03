from django.test import TestCase
from django.core.exceptions import ValidationError
from main.models import Products, Categories, CompleteProducts, Services, Certificates, ContactRequest

class ContactRequestValidationTest(TestCase):

    def test_contact_request_name_required(self):
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

    def setUp(self):
        self.category = Categories.objects.create(title="Категория", slug="kategory")

    def test_valid_product(self):
        product = Products(
            title="Товар 1",
            slug="product-1",
            content={"title": "Товар 1", "brief_desc": "", "description": [], "tables": [], "images": [], "documents": []},
            category=self.category
        )
        # Должен успешно пройти валидацию
        product.full_clean()

    def test_slug_too_short(self):
        product = Products(
            title="Товар 1",
            slug="a",
            content={},
            category=self.category
        )
        with self.assertRaises(ValidationError) as cm:
            product.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_slug_too_long(self):
        product = Products(
            title="Товар 1",
            slug="a"*101,
            content={},
            category=self.category
        )
        with self.assertRaises(ValidationError) as cm:
            product.full_clean()
        self.assertIn('slug', cm.exception.message_dict)


class CategoriesModelValidationTest(TestCase):

    def test_valid_category(self):
        category = Categories(title="Категория", slug="valid-slug")
        category.full_clean()

    def test_slug_too_short(self):
        category = Categories(title="Категория", slug="a")
        with self.assertRaises(ValidationError) as cm:
            category.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_slug_too_long(self):
        category = Categories(title="Категория", slug="a"*101)
        with self.assertRaises(ValidationError) as cm:
            category.full_clean()
        self.assertIn('slug', cm.exception.message_dict)


class CompleteProductsModelValidationTest(TestCase):

    def test_valid_complete_product(self):
        cp = CompleteProducts(name="Завершенный продукт", image_path="path/to/image.jpg")
        cp.full_clean()

    def test_name_required(self):
        cp = CompleteProducts(name="", image_path="path/to/image.jpg")
        with self.assertRaises(ValidationError) as cm:
            cp.full_clean()
        self.assertIn('name', cm.exception.message_dict)

    def test_image_path_required(self):
        cp = CompleteProducts(name="Продукт", image_path="")
        with self.assertRaises(ValidationError) as cm:
            cp.full_clean()
        self.assertIn('image_path', cm.exception.message_dict)


class ServicesModelValidationTest(TestCase):

    def test_valid_service(self):
        service = Services(
            name="Услуга",
            slug="valid-slug",
            content=[{"type": "paragraph", "value": "Описание"}]
        )
        service.full_clean()

    def test_slug_too_short(self):
        service = Services(name="Услуга", slug="a", content=[])
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_slug_too_long(self):
        service = Services(name="Услуга", slug="a"*101, content=[])
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('slug', cm.exception.message_dict)

    def test_name_required(self):
        service = Services(name="", slug="valid-slug", content=[])
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('name', cm.exception.message_dict)

    def test_content_required(self):
        service = Services(name="Услуга", slug="valid-slug", content=None)
        with self.assertRaises(ValidationError) as cm:
            service.full_clean()
        self.assertIn('content', cm.exception.message_dict)


class CertificatesModelValidationTest(TestCase):

    def test_valid_certificate(self):
        cert = Certificates(title="Сертификат")
        cert.full_clean()

    def test_title_required(self):
        cert = Certificates(title="")
        with self.assertRaises(ValidationError) as cm:
            cert.full_clean()
        self.assertIn('title', cm.exception.message_dict)