from django.urls import reverse
from rest_framework.test import APITestCase
from main.models import Product, Category
from unittest.mock import patch

class ProductAPITest(APITestCase):
    """Tests for Products API endpoints."""
    def setUp(self):
        """Set up test data for Products API tests."""
        category = Category.objects.create(id=1, title="Категория", slug="category")
        Product.objects.create(title="Продукт 1", slug="product-1", content={}, category=category)
        
    def test_get_products_success(self):
        """Test retrieving products successfully."""
        url = reverse('get_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['title'], "Продукт 1")
    
    def test_get_products_error_handling(self):
        """Test error handling when retrieving products."""
        with patch('main.views.api.Product.objects.all', side_effect=Exception('fail')):
            url = reverse('get_products')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 500)
            self.assertIn('Ошибка', response.data['message'])

class ContactRequestAPITest(APITestCase):
    """Tests for ContactRequest API endpoints."""
    def test_send_contacts_success(self):
        """Test sending contact request successfully."""
        url = reverse('send_contacts')
        data = {
            'name': 'Тест',
            'phone': '+79998887766',
            'email': 'test@test.com',
            'comment': 'Комментарий'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
    
    def test_send_contacts_invalid(self):
        """Test sending contact request with invalid data."""   
        url = reverse('send_contacts')
        data = {'name': '', 'phone': '', 'email': 'notanemail'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('email', response.data['errors'])
