from rest_framework import serializers
from core.models import Lodge

class LodgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodge
        fields = [
            'id',
            'name',
            'location',
            'total_rooms',
            'rent_rate',
            'caretaker_number',
            'description',
        ]
        read_only_fields = ['id']




