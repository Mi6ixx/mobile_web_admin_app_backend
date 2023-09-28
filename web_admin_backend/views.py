from rest_framework import viewsets, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Lodge
from .serializers import LodgeSerializer

# Create your views here.
class LodgeViewSets(viewsets.ModelViewSet):
    queryset = Lodge.objects.all()
    serializer_class = LodgeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only lodge objects for the request user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new lodges for a specific authenticated user"""
        serializer.save(user=self.request.user)


