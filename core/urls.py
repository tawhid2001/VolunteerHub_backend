from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VolunteerWorkViewSet, ReviewViewSet,UserDetailView,JoinRequestViewSet,CategoryViewSet,CategoryworklistViewSet,has_reviewed

router = DefaultRouter()
router.register('volunteer-work', VolunteerWorkViewSet)
router.register('reviews', ReviewViewSet)
router.register('join-requests', JoinRequestViewSet)
router.register('category-list',CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-works/', VolunteerWorkViewSet.as_view({'get': 'my_works'}), name='my-volunteer-works'),
    path('participated/', VolunteerWorkViewSet.as_view({'get': 'participated_works'}), name='participated-volunteer-works'),
    path('<int:pk>/', VolunteerWorkViewSet.as_view({'get': 'details'}), name='volunteer-work-details'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('list/<slug:slug>/',CategoryworklistViewSet.as_view(), name='category-work-list'),
    path('volunteer-work/<int:volunteer_work_id>/has-reviewed/', has_reviewed, name='has-reviewed'),
]
