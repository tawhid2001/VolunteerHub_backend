from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import VolunteerWork, Review
from .serializers import VolunteerWorkSerializer, ReviewSerializer
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

class VolunteerWorkViewSet(viewsets.ModelViewSet):
    queryset = VolunteerWork.objects.all()
    serializer_class = VolunteerWorkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.organizer != request.user:
            return Response({"detail": "You do not have permission to edit this volunteer work."}, status=403)
        return super().update(request, *args, **kwargs)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.organizer != request.user:
            return Response({"detail": "You do not have permission to delete this volunteer work."}, status=403)
        return super().destroy(request, *args, **kwargs)


    @action(detail=False, methods=['get'])
    def my_works(self, request):
        """List of volunteer work organized by the user."""
        queryset = VolunteerWork.objects.filter(organizer=request.user)
        if not queryset.exists():
            return Response({"detail": "No works found for this user."})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def participated_works(self, request):
        """List of volunteer work the user has participated in."""
        queryset = VolunteerWork.objects.filter(participants=request.user)
        if not queryset.exists():
            return Response({"detail": "No participated works found for this user."})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    queryset = VolunteerWork.objects.all()
    serializer_class = VolunteerWorkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=['get'])
    def my_works(self, request):
        """List of volunteer work organized by the user."""
        queryset = VolunteerWork.objects.filter(organizer=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def participated_works(self, request):
        """List of volunteer work the user has participated in."""
        queryset = VolunteerWork.objects.filter(participants=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Details of a specific volunteer work."""
        queryset = VolunteerWork.objects.get(pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the user can't review the same volunteer work more than once
        volunteer_work = serializer.validated_data['volunteer_work']
        if Review.objects.filter(volunteer_work=volunteer_work, user=self.request.user).exists():
            raise serializers.ValidationError("You have already reviewed this volunteer work.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Allow the user to update their review only
        if self.get_object().user != self.request.user:
            raise serializers.ValidationError("You do not have permission to edit this review.")
        serializer.save()

    def perform_destroy(self, instance):
        # Allow the user to delete their review only
        if instance.user != self.request.user:
            raise serializers.ValidationError("You do not have permission to delete this review.")
        instance.delete()
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

