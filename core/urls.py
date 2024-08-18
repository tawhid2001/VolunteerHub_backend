from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VolunteerWorkViewSet, ReviewViewSet

router = DefaultRouter()
router.register('volunteer-work', VolunteerWorkViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
