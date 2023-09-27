from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'user_type']


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'user_type']
