from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.db.models import Avg
from core.models import Project, Criteria, Rating

User = get_user_model()

class TopProjectRankingTest(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('alice', email='alice@test.com', password='pass123')
        self.u2 = User.objects.create_user('bob', email='bob@test.com', password='pass123')

        self.c = Criteria.objects.create(name="Innovation")

        self.p1 = Project.objects.create(name="Social Media Feed", status='published')
        self.p2 = Project.objects.create(name="Job Platform", status='published')

        Rating.objects.create(user=self.u1, project=self.p1, criteria=self.c, score=5)
        Rating.objects.create(user=self.u2, project=self.p1, criteria=self.c, score=4)

        Rating.objects.create(user=self.u1, project=self.p2, criteria=self.c, score=3)
        Rating.objects.create(user=self.u2, project=self.p2, criteria=self.c, score=2)

    def test_top_project_sorted(self):
        # --- FIX: Added /v1/ ---
        res = self.client.get('/api/v1/projects/top/', format='json')
        
        self.assertEqual(res.status_code, 200)

        # Note: Your 'top' endpoint returns a raw list, so [0] works fine.
        self.assertEqual(res.data[0]['id'], self.p1.id)