from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class ProjectCreationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', 
            email='alice@test.com', 
            password='pass123'
        )

        url = reverse('token_obtain_pair')
        
        response = self.client.post(
            url, 
            {
                'email': 'alice@test.com', 
                'password': 'pass123'
            }, 
            format='json'
        )
        
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_project(self):
        data = {
            'name': 'Online Polling System',
            'description': 'A voting system',
            'category': 'poll' 
        }
        
        # --- FIX: Added /v1/ ---
        res = self.client.post('/api/v1/projects/', data, format='json')
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'Online Polling System')