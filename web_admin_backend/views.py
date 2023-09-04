
from rest_framework import viewsets
from rest_framework import serializers
from .serializers import LodgeSerializer
from .models import Lodge
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

class LodgeViewSet(viewsets.ModelViewSet):
    queryset = Lodge.objects.all()
    serializer_class = LodgeSerializer
    # authentication_classes = [TokenAuthentication]

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




