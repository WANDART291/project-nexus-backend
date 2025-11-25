from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTest(APITestCase):
    def test_user_can_register_and_login(self):
        # Create user with email
        user = User.objects.create_user('alice', email='alice@test.com', password='pass123')
        
        url = reverse('token_obtain_pair')
        
        # ✅ FIX: Use 'email' instead of 'username'
        data = {
            'email': 'alice@test.com', 
            'password': 'pass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)