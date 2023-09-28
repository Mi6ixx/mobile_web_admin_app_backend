from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .serializers import StudentSerializer, StudentImageSerializer, StudentReviewSerializer
from core.models import Student, LodgeReview, Lodge
from rest_framework.decorators import action
from .permission import IsOwnerOfStudent


# Create your views here.
class StudentViewSets(mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """View to manage students"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOfStudent]

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return StudentImageSerializer
        return self.serializer_class

    @action(methods=['POST', 'PUT', 'DELETE'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image for a student object"""
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data)

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
        """Create a new recipe for a specific authenticated user"""
        serializer.save(user=self.request.user)


class StudentReviewViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = LodgeReview.objects.all()
    serializer_class = StudentReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOfStudent]

    def get_queryset(self):
        """Return tags for only the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    @action(methods=['POST'], detail=True)
    def create_review(self, request, pk=None):
        try:
            # Get the specific lodge for which the review will be created
            lodge = Lodge.objects.get(pk=pk)

            # Check if a review already exists for this lodge and user
            existing_review = LodgeReview.objects.filter(user=request.user, lodge=lodge).first()
            if existing_review:
                return Response(
                    {"detail": "You have already reviewed this lodge."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create a new review for the lodge
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, lodge=lodge)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Lodge.DoesNotExist:
            return Response(
                {"detail": "The specified lodge does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
