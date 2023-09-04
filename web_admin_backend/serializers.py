from rest_framework import serializers
from .models import Lodge, CustomUser
from .validators import validate_image_size


class LodgeSerializer(serializers.ModelSerializer):
    # Define a custom ImageField form field
    images = serializers.ImageField(max_length=None, use_url=True,
                                    validators=[validate_image_size])  # use_url=True to display image URLs

    class Meta:
        model = Lodge
        fields = ['name', 'location', 'images', 'total_rooms', 'rent_rate', 'caretaker_number', 'description']

class AdminUserRegistration(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


class AdminUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)
