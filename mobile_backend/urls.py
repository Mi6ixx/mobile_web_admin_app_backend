from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSets, StudentReviewViewSet, FriendRequestViewSet

router = DefaultRouter()
router.register('student', StudentViewSets)
router.register('review', StudentReviewViewSet)
router.register('roommate-request', FriendRequestViewSet)

app_name = 'student'
urlpatterns = [
    path('', include(router.urls)),
]
