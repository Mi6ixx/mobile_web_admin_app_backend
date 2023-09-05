from django.db import models
from django.conf import settings

# Create your models here.

class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "male"
        FEMALE = "F", "female"
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student")
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True, null=True)
    age = models.IntegerField(default=0)
    department = models.CharField(max_length=100)
    year_of_admission = models.CharField(max_length=4)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
