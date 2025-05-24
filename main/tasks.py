from celery import shared_task
from main.utils import NotifyManager
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification_email(contact_id):
    
    NotifyManager.send_mail(contact_id)   