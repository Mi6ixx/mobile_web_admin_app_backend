from django.test import TestCase
from .models import Lodge

class LodgeModelTestCase(TestCase):
    def setUp(self):
        # Create a sample Lodge instance for testing
        self.lodge = Lodge(
            name="Test Lodge",
            location="Test Location",
            total_rooms=5,
            rent_rate=100.50,
            caretaker_number="+1234567890",
            description="Test description"
        )

    def test_lodge_creation(self):
        """Test Lodge model creation."""
        self.lodge.save()
        lodges_count = Lodge.objects.count()
        self.assertEqual(lodges_count, 1)

    def test_lodge_str_representation(self):
        """Test the __str__ method of the Lodge model."""
        self.assertEqual(str(self.lodge), "Test Lodge")

    def test_name_field(self):
        """Test the name field."""
        # Try to create a Lodge with a duplicate name (unique constraint)
        duplicate_lodge = Lodge(
            name="Test Lodge",
            location="Another Location",
            total_rooms=3,
            rent_rate=75.25,
            caretaker_number="+9876543210",
            description="Another description"
        )
        with self.assertRaises(Exception):
            duplicate_lodge.save()

    def test_blank_fields(self):
        """Test blank=False fields for Lodge model."""
        # Attempt to create a Lodge instance with blank=False fields empty
        empty_lodge = Lodge(
            name="Empty Lodge",
            location="",
            total_rooms=None,
            rent_rate=None,
            caretaker_number="",
            description=None
        )
        with self.assertRaises(ValueError):
            empty_lodge.full_clean()

    def test_unique_fields(self):
        """Test unique=True fields for Lodge model."""
        self.lodge.save()

        # Attempt to create another Lodge with the same caretaker_number (unique constraint)
        duplicate_caretaker_lodge = Lodge(
            name="Duplicate Caretaker Lodge",
            location="New Location",
            total_rooms=8,
            rent_rate=120.75,
            caretaker_number="+1234567890",  # Same as the first Lodge
            description="Duplicate description"
        )
        with self.assertRaises(Exception):
            duplicate_caretaker_lodge.save()

    def test_positive_total_rooms(self):
        """Test that total_rooms is a positive integer."""
        self.lodge.total_rooms = -2
        with self.assertRaises(ValueError):
            self.lodge.full_clean()

    def test_positive_rent_rate(self):
        """Test that rent_rate is a positive decimal number."""
        self.lodge.rent_rate = -50.75
        with self.assertRaises(ValueError):
            self.lodge.full_clean()

    def test_valid_phone_number(self):
        """Test that caretaker_number is a valid phone number."""
        self.lodge.caretaker_number = "12345"  # Invalid phone number
        with self.assertRaises(Exception):
            self.lodge.full_clean()
