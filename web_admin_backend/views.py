from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .serializers import LodgeSerializer, AdminUserLoginSerializer, AdminUserRegistration
from .models import Lodge
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .permissions import IsSuperUser, IsAdminUserOrSuperUser
from django.contrib.auth import get_user_model

User = get_user_model()


class LodgeViewSet(viewsets.ModelViewSet):
    queryset = Lodge.objects.all()
    serializer_class = LodgeSerializer
    permission_classes = [IsAdminUserOrSuperUser]  # Applying the custom permission

    @swagger_auto_schema(request_body=serializers.ImageField(help_text='Upload an image for the lodge'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.ImageField(help_text='Upload an image for the lodge'))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.ImageField(help_text='Upload an image for the lodge'))
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminUserRegister(viewsets.ViewSet):
    permission_classes = [IsSuperUser]

    def create(self, request, *args, **kwargs):
        serializer = AdminUserRegistration(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            User.objects.create_admin(username=username, email=email, password=password)
            return Response(
                {'message': 'Admin user created successfully.'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserLogin(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        # Deserialize the login data
        serializer = AdminUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
