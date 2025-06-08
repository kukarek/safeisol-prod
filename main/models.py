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
    - category: Foreign key to the Categories model, allowing products to be categorized.

    Methods:
    - get_absolute_url: Returns the URL for the product detail page.
    - __str__: Returns the title of the product as its string representation.

    Validators:
    - MinLengthValidator: Ensures the slug is at least 5 characters long.
    - MaxLengthValidator: Ensures the slug does not exceed 100 characters.

    """

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.JSONField(verbose_name="Контент") 
    """
    JSON field to store detailed information about the product.
    The structure of the content can include various types of data such as text, images, and tables.
    Example structure:

    content = {
        "title": "",
        "brief_desc": "",
        "description": [
            {"type": "paragraph", "value": ""},
            {"type": "img", "value": ""},
            {"type": "list", "value": {
                "title": "",
                "values": ["", "", ""]
            }}
        ],

        "tables": [
    {
        "header": "Технические данные",
        "columns": ["Параметр", "Значение"],
        "rows": [
            ["", ""],
            ["", ""],
            ["", ""]
        ]
    },
    {
        "header": "Дополнительные характеристики",
        "columns": ["Параметр", "Значение"],
        "rows": [
            ["", ""],
            ["", ""],
            ["", ""]
        ]
    }],
        "images": [
            {"type": "image", "src": ""},
            {"type": "image", "src": ""},
            {"type": "image", "src": ""}
        ],

        "documents": [
            {"name": "", "format": "", "size": "", "src": ""},
            {"name": "", "format": "", "size": "", "src": ""},
            {"name": "", "format": "", "size": "", "src": ""}
        ]
    }
    """

    category = models.ForeignKey('Category', related_name='products', on_delete=models.SET_NULL, null=True, verbose_name="Категория")

    def get_absolute_url(self):
        """
        Returns the URL for the product detail page.
        Uses the product's slug to generate the URL.
        """
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        """
        Returns the title of the product as its string representation.
        This method is used when the object is printed or displayed in the admin interface.
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the URL for the product detail page.
        Uses the product's slug to generate the URL.
        """
        return reverse('product', kwargs={'product_slug': self.slug})


class Category(models.Model):
    """
    Model representing a product category with a slug and title.

    Fields:
    - title: Title of the category.
    - slug: Unique slug for the category, used in URLs.
    - content: JSON field containing additional information about the category.
    - products: Related name for accessing products in this category.

    Methods:
    - __str__: Returns the title of the category as its string representation.
    - get_absolute_url: Returns the URL for the category detail page.

    Validators:
    - MinLengthValidator: Ensures the slug is at least 5 characters long.
    - MaxLengthValidator: Ensures the slug does not exceed 100 characters.
    """

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    def __str__(self):
        """
        Returns the title of the category as its string representation.
        This method is used when the object is printed or displayed in the admin interface.
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the URL for the category detail page.
        Uses the category's slug to generate the URL.
        """
        return reverse('category', kwargs={'category_slug': self.slug})

class CompleteProject(models.Model):
    """
    Model representing a complete project with a name and image path.
    
    Fields:
    - name: Name of the complete project.
    - image_path: Path to the image representing the complete project.
    Methods:
    - __str__: Returns the name of the complete project as its string representation.
    """
    name = models.CharField(max_length=255, verbose_name="Название")
    image_path = models.CharField(max_length=255, verbose_name="Изображение")

    def __str__(self):
        """
        Returns the name of the complete project as its string representation.
        This method is used when the object is printed or displayed in the admin interface.
        """
        return self.name

class Service(models.Model):
    """
    Model representing a service with a name, slug, and content.

    Fields:
    - name: Name of the service.
    - slug: Unique slug for the service, used in URLs.
    - content: JSON field containing detailed information about the service.

    Methods:
    - __str__: Returns the name of the service as its string representation.

    Validators:
    - MinLengthValidator: Ensures the slug is at least 5 characters long.
    - MaxLengthValidator: Ensures the slug does not exceed 100 characters.
    """

    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    
    content = models.JSONField(verbose_name="Контент") 
    """
    JSON field to store detailed information about the service.
    The structure of the content can include various types of data such as text, images, and lists.
    Example structure:

    content = [
    {
        "type": "paragraph",
        "value": ""
    },
    {
        "type": "list",
        "value": {
        "title": "",
        "values": []
        }
    }]
    """

class Certificate(models.Model):
    """
    Model representing a certificate with a title.

    Fields:
    - title: Title of the certificate.

    Methods:
    - __str__: Returns the title of the certificate as its string representation.
    """

    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
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
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает отправки'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)

    def __str__(self):
        """
        Returns a string representation of the contact request, including the name and email.
        This method is used when the object is printed or displayed in the admin interface.
        """
        return f"{self.name} ({self.email})"
    


