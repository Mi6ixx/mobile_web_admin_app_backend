from rest_framework import serializers
from .models import Student 


class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Student 
        fields = ["id", 'user_id', 'gender', 'age', 'department', 'year_of_admission']