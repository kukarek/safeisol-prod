from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.urls import reverse

class Products(models.Model):

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.JSONField(verbose_name="Контент") 
    category = models.ForeignKey('Categories', related_name='products', on_delete=models.SET_NULL, null=True, verbose_name="Категория")

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Categories(models.Model):

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

class CompleteProducts(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название")
    image_path = models.CharField(max_length=255, verbose_name="Изображение")

class Services(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    
    content = models.JSONField(verbose_name="Контент") 

class Certificates(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название")

#входящие заявки от пользователей
class ContactRequest(models.Model):
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Статус заявки
    STATUS_CHOICES = [
        ('pending', 'Ожидает отправки'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    

# Структура json контента

# content = {
#     "title": "",
#     "brief_desc": "",
#     "description": [
#         {"type": "paragraph", "value": ""},
#         {"type": "img", "value": ""},
#         {"type": "list", "value": {
#             "title": "",
#             "values": ["", "", ""]
#         }}
#     ],

#     "tables": [
# {
#     "header": "Технические данные",
#     "columns": ["Параметр", "Значение"],
#     "rows": [
#         ["", ""],
#         ["", ""],
#         ["", ""]
#     ]
# },
# {
#     "header": "Дополнительные характеристики",
#     "columns": ["Параметр", "Значение"],
#     "rows": [
#         ["", ""],
#         ["", ""],
#         ["", ""]
#     ]
# }],
#     "images": [
#         {"type": "image", "src": ""},
#         {"type": "image", "src": ""},
#         {"type": "image", "src": ""}
#     ],

#     "documents": [
#         {"name": "", "format": "", "size": "", "src": ""},
#         {"name": "", "format": "", "size": "", "src": ""},
#         {"name": "", "format": "", "size": "", "src": ""}
#     ]
# }



# структура json обьекта для услуги

# [
#   {
#     "type": "paragraph",
#     "value": ""
#   },
#   {
#     "type": "list",
#     "value": {
#       "title": "",
#       "values": []
#     }
#   }
# ]

