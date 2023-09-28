from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core import models
from django.contrib.auth import get_user_model
from web_admin_backend.serializers import LodgeSerializer

LODGE_URL = reverse('lodge:lodge-list')

def detail_url(lodge_id):
    """Create and return a student detail url"""
    return reverse('lodge:lodge-detail', args=[lodge_id])


def create_user(**params):
    """Create and return user"""
    defaults = {
        'email': 'kodi@example.com',
        'password': 'dffpass123',
        'phone': '08106671579',
        'user_type': 'STUDENT',
        'first_name': 'ookofk',
        'last_name': 'ojodfjdj'
    }
    defaults.update(params)
    user = get_user_model().objects.create_user(**defaults)
    return user


def create_lodge(user, **params):
    """Create and return lodge"""
    defaults = {
        'name': 'St.Domininc lodge',
        'location': 'Opposite laurel junction',
        'total_rooms': 23,
        'rent_rate': 230000,
        'caretaker_number': '0803473998',
    }
    defaults.update(params)
    lodge = models.Lodge.objects.create(user=user, **defaults)

    return lodge


class PublicRecipeApiTests(TestCase):
    """Testing unauthenticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for API request"""
        res = self.client.get(LODGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStudentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)



