"""Test user API"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def create_user(**params):
    """Create and return user"""
    defaults = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'phone': '08106671579',
        'user_type': 'STUDENT',
        'username': 'kodi918'
    }
    defaults.update(params)
    user = get_user_model().objects.create_user(**defaults)
    return user


class PublicUserApiTests(TestCase):
    """Testing public(unauthenticated) features of API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_endpoint_success(self):
        """Test create user endpoint"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'username': 'name',
            'first_name': 'kodi',
            'last_name': 'zaram',
            'user_type': 'STUDENT',
        }
        res = self.client.post('/auth/users/', data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_get_user_tokens(self):
        """Test getting user access and refresh token"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'username': 'name',
            'first_name': 'kodi',
            'last_name': 'zaram',
            'user_type': 'STUDENT',
        }
        user = self.client.post('/auth/users/', data=payload)
        res = self.client.post('/auth/jwt/create', data=payload)
        # print(res.data)
        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user_access_token_refresh(self):
        """Test getting user access being refreshed"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'username': 'name',
            'first_name': 'kodi',
            'last_name': 'zaram',
            'user_type': 'STUDENT',
        }
        self.client.post('/auth/users/', data=payload)
        res = self.client.post('/auth/jwt/create', data=payload)
        payload2 = {
            'refresh': res.data['refresh']
        }
        self.client.post('/auth/jwt/refresh', data=payload2)
        # print(res.data)
        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateUserApiTests(TestCase):
    """Testing authenticated user endpoints"""

    def setUp(self) -> None:
        self.client = APIClient()
        payload = {
            'email': 'testdsd@example.com',
            'password': 'testpass123',
            'username': 'namdde',
            'first_name': 'kdodi',
            'last_name': 'zadsram',
            'user_type': 'STUDENT',
        }
        self.user = create_user(**payload)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_success(self):
        """Test retrieving user details"""
        res = self.client.get('/auth/users/me', follow=True, format='json')
        self.assertEqual(res.data['email'], self.user.email)
        self.assertEqual(res.data['user_type'], self.user.user_type)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_user_model().objects.count(), 1)

    # def test_patch_method_on_user_profile(self):
    #     """Testing PATCH method for this endpoint"""
    # 
    #     payload = {
    #         'email': 'testasa2@example.com',
    #     }
    # 
    #     res = self.client.patch('/auth/users/me', payload, follow=True, format='json')
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.email, payload['email'])
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        """Testing user delete"""
        res = self.client.delete('/auth/users/me', follow=True, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
