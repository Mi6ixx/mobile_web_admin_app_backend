from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LodgeViewSets

router = DefaultRouter()
router.register('lodges', LodgeViewSets)

app_name = 'lodge'

urlpatterns = [
    path('', include(router.urls)),
]