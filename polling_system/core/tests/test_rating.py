from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Project, Criteria

User = get_user_model()

class RatingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', 
            email='alice@test.com', 
            password='pass123'
        )
        
        url = reverse('token_obtain_pair')
        
        response = self.client.post(
            url, 
            {'email': 'alice@test.com', 'password': 'pass123'}, 
            format='json'
        )
        
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # ✅ FIX: Set matching categories so serializer validation passes
        # (Assuming "web" is a valid choice in your models. If not, use a valid one like "mobile")
        self.project = Project.objects.create(name="Movie App", category="web")
        self.criteria = Criteria.objects.create(name="Innovation", project_category="web")

    def test_user_can_rate_project(self):
        url = f'/api/projects/{self.project.id}/ratings/'

        data = {
            # Ensure we use 'criteria_id' as required by your serializer
            'criteria_id': self.criteria.id,
            'score': 5
        }
        
        res = self.client.post(url, data, format='json')
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['score'], 5)