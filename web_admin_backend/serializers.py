from rest_framework import serializers
from .models import Lodge
from .validators import validate_image_size

class LodgeSerializer(serializers.ModelSerializer):
    # Define a custom ImageField form field
    images = serializers.ImageField(max_length=None, use_url=True, validators=[validate_image_size])  # use_url=True to display image URLs

    class Meta:
        model = Lodge
        fields = '__all__'
