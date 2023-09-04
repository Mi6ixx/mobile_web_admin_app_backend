from django.urls import path, include
from rest_framework.routers import DefaultRouter
from views import LodgeListCreateView, LodgeRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'lodges', LodgeListCreateView)

urlpatterns = [
    path('', include(router.urls)),
    path('lodges/<int:pk>/', LodgeRetrieveUpdateDestroyView.as_view(), name='lodge-detail'),
]
