from django.urls import path, include
from .views import SendFriendRequest, AcceptFriendRequest

urlpatterns = [
    path('send-friend-request/<int:to_user_id>/', SendFriendRequest.as_view(), name='send-friend-request'),
    path('accept-friend-request/<int:to_user_id>/', AcceptFriendRequest.as_view(), name='accept-friend-request'),
]
