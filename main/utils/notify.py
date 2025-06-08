import logging
from django.core.mail import send_mail as django_send_mail
from django.conf import settings
from main.models import ContactRequest
from main.serializers import ContactRequestSerializer

logger = logging.getLogger('django')

class NotifyManager:
    """
    Manager for sending notifications.
    This class handles the logic for sending emails when a contact request is created.
    It is designed to be used with Celery tasks.

    Methods:
        send_mail(contact_id) -> None:

    Parameters:
        contact_id (int): The ID of the ContactRequest instance to send an email for.
    """
    @staticmethod
    def send_mail(contact_id) -> None:
        """
        Sends an email notification for a contact request.
        This method retrieves the contact request by its ID, serializes the data,
        and sends an email with the contact details.
        If the email is sent successfully, it updates the status of the contact request to 'sent'.
        If there is an error during the email sending process, it logs the error and updates the status to 'failed'.
        
        Parameters:
            contact_id (int): The ID of the ContactRequest instance to send an email for.
        """
        try:
            contact = ContactRequest.objects.get(pk=contact_id)

            serializer = ContactRequestSerializer(contact)
            data = serializer.data

            message = (
                f"Имя: {data['name']}\n"
                f"Телефон: {data['phone']}\n"
                f"Email: {data['email']}\n\n"
                f"{data['comment']}"
            )

            django_send_mail(
                subject='Новая заявка!',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FOR_EMAIL],
                fail_silently=False,
            )

            contact.status = 'sent'

        except Exception as e:
            logger.error(f"Ошибка отправки письма для заявки {contact_id}: {e}")
            contact.status = 'failed'

        finally:
            contact.save()
            logger.info(f"Статус заявки {contact_id} обновлен на {contact.status}")