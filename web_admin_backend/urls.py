from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LodgeViewSet

router = DefaultRouter()
router.register(r'lodges', LodgeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('lodges/<int:pk>/', LodgeRetrieveUpdateDestroyView.as_view(), name='lodge-detail'),
]
