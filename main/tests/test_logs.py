import logging
from django.test import TestCase

class LoggingTest(TestCase):
    """Tests for logging output in Django."""
    def test_logging_output(self):
        """Test that logging outputs the expected message."""
        logger = logging.getLogger('django')  

        with self.assertLogs(logger, level='INFO') as cm:
            logger.info('Тестовое лог-сообщение')

        # Проверяем, что нужное сообщение появилось в логах
        self.assertIn('Тестовое лог-сообщение', cm.output[0])