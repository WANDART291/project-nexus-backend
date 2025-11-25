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

        # ✅ FIX: Set matching categories here too
        self.project = Project.objects.create(name="Ecommerce Catalog", category="web")
        self.criteria = Criteria.objects.create(name="Design", project_category="web")

    def test_user_cannot_rate_twice(self):
        url = f'/api/projects/{self.project.id}/ratings/'
        
        payload = {
            'criteria_id': self.criteria.id, 
            'score': 4
        }

        # First vote: Should succeed
        first = self.client.post(url, payload, format='json')
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)

        # Second vote: Should fail (Duplicate)
        second = self.client.post(url, payload, format='json')
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)