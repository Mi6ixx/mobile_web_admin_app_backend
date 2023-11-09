from rest_framework import serializers
from core.models import CustomUser, FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status']
        read_only_fields = ['id']
