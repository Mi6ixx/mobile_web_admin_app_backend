from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = "STUDENT", "student"
        LANDLORD = "LANDLORD", "landlord"
    
    
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=11)
    user_type = models.CharField(max_length=20, choices=UserType.choices, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email