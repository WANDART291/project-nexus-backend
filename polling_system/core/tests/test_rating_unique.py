from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from core.models import Project, Criteria

User = get_user_model()

class UniqueRatingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bob', 
            email='bob@test.com', 
            password='pass123'
        )

        url = reverse('token_obtain_pair')

        response = self.client.post(
            url, 
            {'email': 'bob@test.com', 'password': 'pass123'}, 
            format='json'
        )
        
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.project = Project.objects.create(name="Ecommerce Catalog", category="web")
        self.criteria = Criteria.objects.create(name="Design", project_category="web")

    def test_user_cannot_rate_twice(self):
        # --- FIX: Added /v1/ ---
        url = f'/api/v1/projects/{self.project.id}/ratings/'
        
        payload = {
            'criteria_id': self.criteria.id, 
            'score': 4
        }

        first = self.client.post(url, payload, format='json')
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)

        second = self.client.post(url, payload, format='json')
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)