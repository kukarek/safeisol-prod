import logging
from django.core.mail import send_mail as django_send_mail
from django.conf import settings
from main.models import ContactRequest
from main.serializers import ContactRequestSerializer

logger = logging.getLogger('django')

class NotifyManager:
    """
    Manager for sending notifications via email when a contact request is created.
    This class provides a static method to send an email with the details of the contact request.
    """
    
    @staticmethod
    def send_mail(contact_id) -> None:
        try:
            contact = ContactRequest.objects.get(pk=contact_id)
        except ContactRequest.DoesNotExist:
            logger.error(f"ContactRequest с id={contact_id} не найден.")
            return

        serializer = ContactRequestSerializer(contact)
        data = serializer.data

        message = f"""
Имя: {data['name']}
Телефон: {data['phone']}
Email: {data['email']}

{data['comment']}
""".strip()

        try:
            django_send_mail(
                subject='Новая заявка!',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FOR_EMAIL],
                fail_silently=False,
            )
            contact.status = 'sent'
            logger.info(f"Письмо успешно отправлено для заявки {contact_id}.")
        except Exception as e:
            logger.error(f"Ошибка отправки письма для заявки {contact_id}: {e}")
            contact.status = 'failed'
            contact.error_message = str(e)  # Можно сохранять ошибку в модели

        contact.save()
        logger.info(f"Статус заявки {contact_id} обновлен на {contact.status}")
