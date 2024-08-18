from rest_framework import serializers
from .models import VolunteerWork, Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'volunteer_work', 'user', 'rating', 'rating_display', 'comment', 'created_at']

class VolunteerWorkSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = VolunteerWork
        fields = ['id', 'title', 'description', 'location', 'date', 'organizer', 'participants', 'category', 'average_rating']

    def get_average_rating(self, obj):
        return obj.average_rating()
