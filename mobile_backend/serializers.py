from rest_framework import serializers
from core.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for model students"""

    class Meta:
        model = Student
        fields = ['id', 'department', 'year_of_admission', 'gender']
        read_only_fields = ['id']

class StudentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'image']
        read_only_fields = ['id']