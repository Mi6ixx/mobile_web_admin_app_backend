from django.urls import path, include
from .views import SendFriendRequest, AcceptFriendRequest, FriendRequestList, AcceptedFriendRequestList, \
    PendingFriendRequestList, DeclinedFriendRequestList, RemoveFriendRequest, DeclineFriendRequest

urlpatterns = [
    path('get-friend-requests/', FriendRequestList.as_view(), name='friend-request-list'),
    path('accepted-friend-requests/', AcceptedFriendRequestList.as_view(), name='accepted-friend-request-list'),
    path('pending-friend-requests/', PendingFriendRequestList.as_view(), name='pending-friend-request-list'),
    path('declined-friend-requests/', DeclinedFriendRequestList.as_view(), name='declined-friend-request-list'),

    path('remove-friend-request/<int:friend_request_id>/', RemoveFriendRequest.as_view(), name='remove-friend-request'
                                                                                               '-list'),
    path('decline-friend-request/<int:to_user_id>/', DeclineFriendRequest.as_view(), name='declined-friend-request'),
    path('send-friend-request/<int:to_user_id>/', SendFriendRequest.as_view(), name='send-friend-request'),
    path('accept-friend-request/<int:friend_request_id>/', AcceptFriendRequest.as_view(), name='accept-friend-request'),
]
