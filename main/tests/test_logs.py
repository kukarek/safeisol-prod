import logging
from django.test import TestCase

class LoggingTest(TestCase):
    def test_logging_output(self):
        logger = logging.getLogger('django')  

        with self.assertLogs(logger, level='INFO') as cm:
            logger.info('Тестовое лог-сообщение')

        # Проверяем, что нужное сообщение появилось в логах
        self.assertIn('Тестовое лог-сообщение', cm.output[0])