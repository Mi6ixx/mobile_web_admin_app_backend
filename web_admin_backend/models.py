from django.db import models
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Lodge(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    location = models.CharField(max_length=200, null=False, blank=False)
    images = models.ImageField(upload_to='lodges/images/')
    total_rooms = models.IntegerField()
    rent_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    caretaker_number = PhoneNumberField(null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.name