import logging
from django.http import JsonResponse
from main import models
from main.forms import ContactForm
from main.models import ContactRequest
from main import tasks

# Настройка логгера
logger = logging.getLogger(__name__)


# Получение списка продуктов
def get_products(request):
    try:
        # Оптимизация запросов, чтобы избежать множества запросов к базе данных
        products = models.Products.objects.all().values('id', 'title', 'slug')  # Получаем только нужные поля
        product_ids = [product['id'] for product in products]  # Собираем id продуктов
        product_dict = {product.id: product.get_absolute_url() for product in models.Products.objects.filter(id__in=product_ids)}  # Получаем URL для всех продуктов

        products_with_urls = [
            {
                'id': product['id'],
                'title': product['title'],
                'url': product_dict.get(product['id'], '')  # Извлекаем URL из словаря
            }
            for product in products
        ]

        return JsonResponse(products_with_urls, safe=False)
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        return JsonResponse({'success': False, 'message': 'Произошла ошибка при получении продуктов.'})

# Обработка отправки контактной формы
def send_contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            tasks.send_notification_email.delay(form.cleaned_data)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

