from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import CustomUser

class ProductAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com', password='password123')

    def test_create_product(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Product',
            'description': 'Test description',
            'detailed_description': 'Test description',
            'category': 1,
            'price': 10.0,
            'in_stock': True
        }

        response = self.client.post('/api/v1/products/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue('id' in response.data) 
        self.assertEqual(response.data['title'], 'Product') 
        self.assertEqual(response.data['description'], 'Test description') 
        self.assertEqual(response.data['detailed_description'], 'Test description') 
        self.assertEqual(response.data['category'], 1)  
        self.assertEqual(response.data['price'], '10.00')  
