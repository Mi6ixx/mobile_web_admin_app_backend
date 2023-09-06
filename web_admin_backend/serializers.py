from rest_framework import serializers
from .models import Lodge
from .validators import validate_image_size


class LodgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lodge
        fields = ['name', 'location', 'images', 'total_rooms', 'rent_rate', 'caretaker_number', 'description']

# class AdminUserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password']

    # def create(self, validated_data):
    #     return CustomUser.objects.create_admin(**validated_data)


# class AdminUserLoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=30, required=True, write_only=True)
#     password = serializers.CharField(max_length=128, required=True, write_only=True)

    # class Meta:
    #     model = CustomUser
    #     fields = ['username', 'password']
