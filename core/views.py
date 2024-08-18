from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import VolunteerWork, Review
from .serializers import VolunteerWorkSerializer, ReviewSerializer

class VolunteerWorkViewSet(viewsets.ModelViewSet):
    queryset = VolunteerWork.objects.all()
    serializer_class = VolunteerWorkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

