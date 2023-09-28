from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSets, StudentReviewViewSet

router = DefaultRouter()
router.register('student', StudentViewSets)
router.register('review', StudentReviewViewSet)

app_name = 'student'
urlpatterns = [
    path('', include(router.urls)),
]
