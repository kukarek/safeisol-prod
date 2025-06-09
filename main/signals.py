from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContactRequest
from .tasks import send_notification_email


@receiver(post_save, sender=ContactRequest)
def send_email(sender, instance, created, **kwargs) -> None:
    """
    Signal handler that triggers after a ContactRequest instance is saved.

    Sends an email notification asynchronously via Celery
    only if a new ContactRequest has been created.
    """
    if created:
        send_notification_email.delay(instance.pk)
