from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LodgeViewSets, AmenityViewSets

router = DefaultRouter()
router.register('lodges', LodgeViewSets)
router.register('amenities', AmenityViewSets)

app_name = 'lodge'

urlpatterns = [
    path('', include(router.urls)),
]