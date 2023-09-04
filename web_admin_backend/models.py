from django.db import models
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Lodge(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    location = models.CharField(max_length=200, null=False, blank=False)
    images = models.ImageField(upload_to='lodges/images/', null=False, blank=False)
    total_rooms = models.IntegerField()
    rent_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    caretaker_number = PhoneNumberField(null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.name


class AdminUserRegistration(models.Model):
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)  # Store the password securely (e.g., hashed)

    def __str__(self):
        return self.username
