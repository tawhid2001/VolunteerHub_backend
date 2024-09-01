from rest_framework import serializers
from .models import VolunteerWork, Review,Profile,User,JoinRequest,Category
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_null=True)
    contact_info = serializers.CharField(required=False, allow_null=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['profile_picture'] = self.validated_data.get('profile_picture', '')
        data['bio'] = self.validated_data.get('bio', '')
        data['contact_info'] = self.validated_data.get('contact_info', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        # Create Profile
        profile_data = {
            'profile_picture': self.cleaned_data.get('profile_picture'),
            'bio': self.cleaned_data.get('bio'),
            'contact_info': self.cleaned_data.get('contact_info'),
        }
        Profile.objects.create(user=user, **profile_data)

        return user

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    rating_display = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'volunteer_work', 'user', 'rating', 'rating_display', 'comment', 'created_at']

    def get_rating_display(self, obj):
        return '⭐' * obj.rating

class VolunteerWorkSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = VolunteerWork
        fields = ['id', 'title', 'description', 'location', 'date', 'organizer', 'participants', 'category', 'average_rating']

    def get_average_rating(self, obj):
        return obj.average_rating()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class JoinRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    volunteer_work = serializers.PrimaryKeyRelatedField(queryset=VolunteerWork.objects.all())

    class Meta:
        model = JoinRequest
        fields = ['id', 'volunteer_work', 'user', 'status', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

