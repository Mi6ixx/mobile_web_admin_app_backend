from rest_framework import serializers
from .models import Lodge


class LodgeSerializer(serializers.ModelSerializer):
    # Define a custom ImageField form field
    images = serializers.ImageField(max_length=None, use_url=True)  # use_url=True to display image URLs

    class Meta:
        model = Lodge
        fields = '__all__'
