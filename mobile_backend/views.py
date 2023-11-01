from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .serializers import StudentSerializer, StudentImageSerializer, StudentReviewSerializer, FriendRequestSerializer
from core.models import Student, LodgeReview, Lodge, FriendRequest
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


class FriendRequestViewSet(viewsets.GenericViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['POST'])
    def send_request(self, request):
        """
        Send a friend request to a user.
        """
        from_user = request.user  # The sender is the authenticated user
        to_user = self.get_object().to_user  # The recipient is the user associated with the friend request

        if from_user == to_user:
            return Response({'detail': 'You cannot send a friend request to yourself.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if a friend request already exists between these users
        existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()
        if existing_request:
            return Response({'detail': 'A friend request already exists between these users.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create a new friend request
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def accept_request(self, request, pk=None):
        """
        Accept a friend request.
        """
        friend_request = self.get_object()
        to_user = friend_request.to_user
        from_user = friend_request.from_user

        if request.user != to_user:
            return Response({'detail': 'You do not have permission to accept this request.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Add the sender (from_user) to the recipient's (to_user) friends list
        to_user.friends.add(from_user)

        # Update the friend request status to 'accepted'
        friend_request.status = 'accepted'
        friend_request.save()

        return Response({'detail': 'Friend request accepted.'}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def delete_request(self, request, pk=None):
        """Delete a user's request"""
        friend_request = self.get_object()
        to_user = friend_request.to_user
        from_user = friend_request.from_user

        if request.user != to_user:
            return Response({'detail': 'You do not have permission to accept this request.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Delete the friend request
        friend_request.status = 'declined'
        friend_request.delete()

    @action(detail=False, methods=['GET'])
    def pending_requests(self, request):
        """
        List pending friend requests.
        """
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def accepted_requests(self, request):
        """
        List accepted friend requests.
        """
        accepted_requests = FriendRequest.objects.filter(
            Q(from_user=request.user, status='accepted') | Q(to_user=request.user, status='accepted'))
        serializer = self.get_serializer(accepted_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def declined_requests(self, request):
        """
        List declined friend requests.
        """
        declined_requests = FriendRequest.objects.filter(
            Q(from_user=request.user, status='declined') | Q(to_user=request.user, status='declined'))
        serializer = self.get_serializer(declined_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
