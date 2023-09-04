from django.shortcuts import render
from rest_framework import generics
from serializers import LodgeSerializer
from .models import Lodge

# Create your views here.
class LodgeListCreateView(generics.ListCreateAPIView):
    queryset = Lodge.objects.all()
    serializer_class = LodgeSerializer


class LodgeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lodge.objects.all()
    serializer_class = LodgeSerializer
