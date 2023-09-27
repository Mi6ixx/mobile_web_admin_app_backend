from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = "STUDENT", "student"
        LANDLORD = "LANDLORD", "landlord"

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=11)
    user_type = models.CharField(max_length=20, choices=UserType.choices, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    lodges = models.ManyToManyField('Lodge')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email


class Student(models.Model):
    class Gender(models.TextChoices):
        STUDENT = "MALE", "male"
        LANDLORD = "FEMALE", "female"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    department = models.CharField(max_length=100, null=True)
    year_of_admission = models.IntegerField(validators=[
        MinValueValidator(1900),
        MaxValueValidator(2100),
    ], null=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.year_of_admission is not None and len(str(self.year_of_admission)) != 4:
            raise ValidationError({'year_of_admission': 'Year of admission must be a 4-digit number.'})
        if self.year_of_admission is not None and (self.year_of_admission < 1900 or self.year_of_admission > 2100):
            raise ValidationError({'year_of_admission': 'Ensure this value is greater than or equal to 1900.'})

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Lodge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    location = models.CharField(max_length=255, null=False, blank=False)
    total_rooms = models.IntegerField()
    rent_rate = models.IntegerField(null=False, blank=False)
    caretaker_number = models.CharField(max_length=11, null=False, blank=False, unique=True)
    description = models.TextField(max_length=255, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lodge"
        verbose_name_plural = "Lodges"
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
