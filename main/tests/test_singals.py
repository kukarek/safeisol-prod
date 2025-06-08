from django.test import TestCase
from unittest.mock import patch
from main.models import ContactRequest
from main.tasks import send_notification_email  # твоя задача отправки письма

class ContactRequestSignalIntegrationTest(TestCase):
    """Tests for ContactRequest model signals and tasks integration."""
    def test_signal_and_status_update(self):
        """Test that the signal triggers email sending and updates status."""
        contact = ContactRequest.objects.create(
            name="Test",
            phone="+79998887766",
            email="test@test.com",
            comment="Test"
        )
        # Проверяем, что статус изначально 'pending'
        self.assertEqual(contact.status, 'pending')
        # Теперь "выполняем" задачу отправки (вызываем функцию напрямую)
        # Для теста можно замокать фактическую отправку почты, если есть
        with patch('main.tasks.send_notification_email') as mock_send_email:
            mock_send_email.return_value = True  # Имитация успешной отправки
            
            # Вызываем задачу, которая должна обновить статус
            send_notification_email(contact.pk)

        # Обновляем объект из базы, чтобы проверить изменения
        contact.refresh_from_db()
        # Проверяем, что статус стал 'sent'
        self.assertEqual(contact.status, 'sent')
