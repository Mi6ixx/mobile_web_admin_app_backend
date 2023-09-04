from rest_framework import serializers
from .models import Lodge


class LodgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodge
        fields = '__all__'
