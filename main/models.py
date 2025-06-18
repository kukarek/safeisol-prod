from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.urls import reverse


class Product(models.Model):
    """
    Model representing a product with a slug, title, content, and category.

    Fields:
    - slug: Unique slug for the product, used in URLs.
    - title: Title of the product.
    - content: JSON field containing detailed information about the product.
    - category: Foreign key to the Category model, allowing products to be categorized.

    Methods:
    - get_absolute_url: Returns the URL for the product detail page.
    - __str__: Returns the title of the product as its string representation.

    Validators:
    - MinLengthValidator: Ensures the slug is at least 5 characters long.
    - MaxLengthValidator: Ensures the slug does not exceed 100 characters.
    """

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Slug",
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ],
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.JSONField(verbose_name="Контент")
    category = models.ForeignKey(
        "Category",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id"]

    def get_absolute_url(self) -> str:
        """
        Returns the URL for the product detail page.
        Uses the product's slug to generate the URL.
        """
        return reverse("product", kwargs={"product_slug": self.slug})

    def __str__(self) -> str:
        """
        Returns the title of the product as its string representation.
        """
        return self.title


class Category(models.Model):
    """
    Model representing a product category with a slug and title.

    Fields:
    - title: Title of the category.
    - slug: Unique slug for the category, used in URLs.

    Methods:
    - __str__: Returns the title of the category as its string representation.
    - get_absolute_url: Returns the URL for the category detail page.

    Validators:
    - MinLengthValidator: Ensures the slug is at least 5 characters long.
    - MaxLengthValidator: Ensures the slug does not exceed 100 characters.
    """

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Slug",
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ],
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("category", kwargs={"category_slug": self.slug})


class CompleteProject(models.Model):
    """
    Model representing a complete project with a name and image path.

    Fields:
    - name: Name of the complete project.
    - image_path: Path to the image representing the complete project.
    """

    name = models.CharField(max_length=255, verbose_name="Название")
    image_path = models.CharField(max_length=255, verbose_name="Изображение")

    def __str__(self) -> str:
        return self.name


class Service(models.Model):
    """
    Model representing a service with a name, slug, and content.

    Fields:
    - name: Name of the service.
    - slug: Unique slug for the service, used in URLs.
    - content: JSON field containing detailed information about the service.

    Validators:
    - MinLengthValidator: Ensures the slug is at least 5 characters long.
    - MaxLengthValidator: Ensures the slug does not exceed 100 characters.
    """

    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Slug",
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ],
    )
    content = models.JSONField(verbose_name="Контент")

    def __str__(self) -> str:
        return self.name


class Certificate(models.Model):
    """
    Model representing a certificate with a title.

    Fields:
    - title: Title of the certificate.
    """

    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self) -> str:
        return self.title


class ContactRequest(models.Model):
    """
    Model representing a contact request submitted by a user.

    Fields:
    - name: Name of the user submitting the request.
    - phone: Phone number of the user.
    - email: Email address of the user.
    - comment: Additional comment or message from the user.
    - created_at: Timestamp of when the request was created.
    - status: Status of the request (pending, sent, failed).
    - error_message: Error message if the request failed to send.
    """

    STATUS_PENDING = "pending"
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Ожидает отправки"),
        (STATUS_SENT, "Отправлено"),
        (STATUS_FAILED, "Ошибка"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    error_message = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"
