from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LodgeViewSet

router = DefaultRouter()
router.register(r'lodges', LodgeViewSet, basename='lodge-listings')
# router.register(r'login', AdminUserLogin, basename='admin-user-login')
# router.register(r'register', AdminUserRegister, basename='admin-user-registration')

urlpatterns = [
    path('', include(router.urls)),
]
