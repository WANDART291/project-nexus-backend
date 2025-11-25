from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class ProjectCreationTest(APITestCase):
    def setUp(self):
        # 1. Create the user with a specific email
        self.user = User.objects.create_user(
            username='alice', 
            email='alice@test.com', 
            password='pass123'
        )

        # 2. Get the login URL
        url = reverse('token_obtain_pair')
        
        # 3. Log in
        # ✅ FIX: Changed the key from 'username' to 'email' 
        # and used the email address 'alice@test.com'
        response = self.client.post(
            url, 
            {
                'email': 'alice@test.com', 
                'password': 'pass123'
            }, 
            format='json'
        )
        
        # Now this will succeed because the login returned 200 OK
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_project(self):
        data = {
            'name': 'Online Polling System',
            'description': 'A voting system'
        }
        
        res = self.client.post('/api/projects/', data, format='json')
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'Online Polling System')