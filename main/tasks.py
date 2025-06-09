from celery import shared_task
from main.services import NotifyManager
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_email(self, contact_id) -> None:
    """
    Celery task to send notification email for a contact request.
    This task is triggered by the ContactRequest model's post_save signal.
    Retries up to 3 times in case of failure, with 60 seconds delay.
    """
    try:
        NotifyManager.send_mail(contact_id)
    except Exception as exc:
        logger.error(f"Failed to send notification email for contact {contact_id}: {exc}")
        raise self.retry(exc=exc)
