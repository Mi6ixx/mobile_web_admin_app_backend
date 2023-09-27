from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSets

router = DefaultRouter()
router.register('student', StudentViewSets)

app_name = 'student'
urlpatterns = [
    path('', include(router.urls)),
]
