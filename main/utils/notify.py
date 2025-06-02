import logging
from django.core.mail import send_mail as django_send_mail
from django.conf import settings
from main.models import ContactRequest
from main.serializers import ContactRequestSerializer

logger = logging.getLogger(__name__)

class NotifyManager:
    @staticmethod
    def send_mail(contact_id) -> None:
        try:
            # Получаем объект ContactRequest
            contact = ContactRequest.objects.get(pk=contact_id)

            # Сериализуем данные
            serializer = ContactRequestSerializer(contact)
            data = serializer.data

            # Формируем сообщение
            message = (
                f"Имя: {data['name']}\n"
                f"Телефон: {data['phone']}\n"
                f"Email: {data['email']}\n\n"
                f"{data['comment']}"
            )

            # Отправка email
            django_send_mail(
                subject='Новая заявка!',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FOR_EMAIL],
                fail_silently=False,
            )

            # Изменяем статус, если отправка успешна
            contact.status = 'sent'

        except Exception as e:
            logger.error(f"Ошибка отправки письма для заявки {contact_id}: {e}")
            contact.status = 'failed'

        finally:
            contact.save()
            logger.info(f"Статус заявки {contact_id} обновлен на {contact.status}")