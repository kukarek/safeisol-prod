from celery import shared_task
from main.utils import NotifyManager
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification_email(contact_id):
    """
    Celery task to send notification email for a contact request.
    This task is triggered by the ContactRequest model's post_save signal.
    """
    NotifyManager.send_mail(contact_id)   