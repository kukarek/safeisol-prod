import logging
from django.core.mail import send_mail as django_send_mail
from django.conf import settings
from main.models import ContactRequest

# Настройка логирования
logger = logging.getLogger(__name__)

class NotifyManager:
    @staticmethod
    def send_mail(contact_id) -> None:
        
        contact = ContactRequest.objects.get(pk=contact_id)

        try:
            # Отправка email
            django_send_mail(
                subject='Новая заявка!',
                message=f'Имя: {contact.name},\n{contact.phone},\n{contact.email}\n\n{contact.comment}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FOR_EMAIL],
                fail_silently=False,
            )
            
            # Если отправка успешна, изменяем статус
            contact.status = 'sent'

        except Exception as e:
            # Если возникла ошибка, логируем ее и обновляем статус
            logger.error(f"Ошибка отправки письма для заявки {contact.id}: {e}")
            contact.status = 'failed'

        finally:
            # Сохраняем контакт с новым статусом
            contact.save()

