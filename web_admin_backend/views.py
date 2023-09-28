from rest_framework import viewsets, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Lodge, LodgeAmenity
from .serializers import LodgeSerializer, LodgeImageSerializer, LodgeAmenitySerializer
from .permissions import IsAdminOrStaffUser


# Create your views here.
class LodgeViewSets(viewsets.ModelViewSet):
    queryset = Lodge.objects.all()
    serializer_class = LodgeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def get_queryset(self):
        """Return only lodge objects for the request user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return LodgeImageSerializer
        return self.serializer_class

    @action(methods=['POST', 'PUT', 'DELETE'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image for a lodge object"""
        lodge = self.get_object()
        serializer = self.get_serializer(lodge, data=request.data)

        if serializer.is_valid():
            serializer.save()
            # Return the appropriate status code based on the HTTP method
            if request.method == 'POST':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif request.method == 'PUT':
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'DELETE':
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Create a new lodges for a specific authenticated user"""
        serializer.save(user=self.request.user)

class AmenityViewSets(mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = LodgeAmenity.objects.all()
    serializer_class = LodgeAmenitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def get_queryset(self):
        """Return tags for only the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

