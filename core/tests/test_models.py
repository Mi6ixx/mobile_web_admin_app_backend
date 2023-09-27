from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core import models
from django.contrib.auth import get_user_model


def create_user(**params):
    """Create and return user"""
    defaults = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'phone': '08106671579',
        'user_type': 'STUDENT',
        'first_name': 'ookofk',
        'last_name': 'ojodfjdj'
    }
    defaults.update(params)
    user = get_user_model().objects.create_user(**defaults)
    return user


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_success(self):
        """Test creating a user successfully"""
        email = 'kodi@example.com'
        password = 'testpass12345'
        user = create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_blank_email(self):
        """Test creating user with blank email """
        with self.assertRaises(ValueError):
            create_user(email='', password='testpass')

    def test_create_user_with_admin_false(self):
        """Test creating user with admin flag false"""
        user = create_user()
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        """Test creation of superuser"""
        email = 'test@example.com'
        password = '123456789'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
