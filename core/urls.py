from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VolunteerWorkViewSet, ReviewViewSet

router = DefaultRouter()
router.register('volunteer-work', VolunteerWorkViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-works/', VolunteerWorkViewSet.as_view({'get': 'my_works'}), name='my-volunteer-works'),
    path('participated/', VolunteerWorkViewSet.as_view({'get': 'participated_works'}), name='participated-volunteer-works'),
    path('<int:pk>/', VolunteerWorkViewSet.as_view({'get': 'details'}), name='volunteer-work-details'),
]
