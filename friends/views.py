from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import CustomUser, FriendRequest
from .serializers import FriendRequestSerializer


class FriendRequestList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Retrieve all friend requests related to the user
        friend_requests = FriendRequest.objects.filter(to_user=user)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data)


class PendingFriendRequestList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        #       Retrieve all pending friend request to the user
        pending_friend_request = FriendRequest.objects.filter(to_user=user, status='pending')
        serializer = FriendRequestSerializer(pending_friend_request, many=True)
        return Response(serializer.data)


class AcceptedFriendRequestList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        #       Retrieve all accepted friend request to the user
        accepted_friend_request = FriendRequest.objects.filter(to_user=user, status='accepted')
        serializer = FriendRequestSerializer(accepted_friend_request, many=True)
        return Response(serializer.data)


class DeclinedFriendRequestList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        #       Retrieve all declined friend request to the user
        declined_friend_request = FriendRequest.objects.filter(to_user=user, status='declined')
        serializer = FriendRequestSerializer(declined_friend_request, many=True)
        return Response(serializer.data)


class SendFriendRequest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, to_user_id):
        from_user = request.user
        try:
            to_user = CustomUser.objects.get(pk=to_user_id)

        except CustomUser.DoesNotExist:
            return Response(data={'message': 'user_id does not exist in database.Try again!'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if a friend request already exists between these users
        existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()
        if existing_request:
            return Response({'detail': 'A friend request already exists between these users.'},
                            status=status.HTTP_400_BAD_REQUEST)

        elif from_user != to_user:
            serializer = FriendRequestSerializer(data={'from_user': from_user.id, 'to_user': to_user.id})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Cannot send a friend request to yourself", status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_request_id):
        user = request.user
        try:
            friend_request = FriendRequest.objects.filter(pk=friend_request_id, to_user=user, status='pending')
        except FriendRequest.DoesNotExist:
            return Response("Friend request not found or already accepted/declined", status=status.HTTP_404_NOT_FOUND)

        FriendRequest.objects.filter(pk=friend_request_id).update(status='accepted')
        return Response("Friend request accepted", status=status.HTTP_200_OK)


class DeclineFriendRequest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_request_id):
        user = request.user
        try:
            friend_request = FriendRequest.objects.get(pk=friend_request_id, to_user=user, status='pending')
        except FriendRequest.DoesNotExist:
            return Response("Friend request not found or already accepted/declined", status=status.HTTP_404_NOT_FOUND)

        FriendRequest.objects.filter(pk=friend_request_id).update(status='declined')
        return Response("Friend request declined", status=status.HTTP_200_OK)


class RemoveFriendRequest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, friend_request_id):
        user = request.user
        try:
            friend_request = FriendRequest.objects.get(pk=friend_request_id, from_user=user, status='pending')
        except FriendRequest.DoesNotExist:
            return Response("Friend request not found or already accepted/declined", status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        return Response("Friend request removed", status=status.HTTP_204_NO_CONTENT)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5NjE0NDI1LCJqdGkiOiI3MGUwM2RhMzAzZDQ0ODI2ODAxZmU2MGU4YmRkYzE4MCIsInVzZXJfaWQiOjF9.JRzpsSmKO-tl5fgfCBPnb2e5O4N4IukXKwREUU-0xfI
