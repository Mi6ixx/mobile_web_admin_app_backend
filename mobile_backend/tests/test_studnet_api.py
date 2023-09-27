from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core import models
from django.contrib.auth import get_user_model
from mobile_backend.serializers import StudentSerializer

STUDENT_URL = reverse('student:student-list')
def detail_url(student_id):
    """Create and return a student detail url"""
    return reverse('student:student-detail', args=[student_id])


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


def create_student(user, **params):
    defaults = {
        'department': 'science edu',
        'year_of_admission': 2049,
        'gender': 'MALE'
    }
    defaults.update(params)
    student = models.Student.objects.create(user=user, **defaults)

    return student


class PublicRecipeApiTests(TestCase):
    """Testing unauthenticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for API request"""
        res = self.client.get(STUDENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStudentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        # Check if a Student object already exists for the user
        if not hasattr(self.user, 'student'):
            create_student(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_list_student_success(self):
        """Test student creates endpoint"""

        res = self.client.get(STUDENT_URL)
        student = models.Student.objects.filter(user=self.user).first()
        serializer = StudentSerializer(student)

        # print(res.data)
        # print(serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    def test_student_patch_update(self):
        """Test student patch update"""
        student = models.Student.objects.filter(user=self.user).first()
        url = detail_url(student_id=student.id)
        payload = {
            'department': 'science edu',
            'gender': 'MALE'
        }
        res = self.client.patch(url, payload, format='json')

        student.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['gender'], payload['gender'])
        self.assertEqual(res.data['department'], payload['department'])

    def test_full_student_update(self):
        """Test student full update"""

        student = models.Student.objects.filter(user=self.user).first()
        url = detail_url(student_id=student.id)
        payload = {
            'department': 'science edu',
            'year_of_admission': 2049,
            'gender': 'MALE'
        }
        res = self.client.put(url, payload, format='json')

        student.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['gender'], payload['gender'])
        self.assertEqual(res.data['department'], payload['department'])
        self.assertEqual(res.data['year_of_admission'], payload['year_of_admission'])

    def test_year_of_admission_validation(self):
        """Test student full update"""
        invalid_year = 1899  # An invalid year (outside the allowed range)
        student = models.Student.objects.filter(user=self.user).first()
        url = detail_url(student_id=student.id)
        payload = {
            'year_of_admission': invalid_year,

        }
        res = self.client.patch(url, payload, format='json')
        student.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year_of_admission', res.data)
        self.assertEqual(
            res.data['year_of_admission'][0],
            'Ensure this value is greater than or equal to 1900.'
        )
        # Ensure that the student's year_of_admission did not change
        self.assertNotEqual(student.year_of_admission, invalid_year)

    def test_delete_student(self):
        """Test deleting student object"""
        student = models.Student.objects.filter(user=self.user).first()
        url = detail_url(student_id=student.id)
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Student.objects.filter(user=self.user).exists())
