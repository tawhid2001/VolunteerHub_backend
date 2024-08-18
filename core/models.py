from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STAR_CHOICES = [
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐'),
]

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True,default='./image/default_profile.jpg')
    contact_info = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.username
    

class VolunteerWork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    organizer = models.ForeignKey(User, related_name='organized_works', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participated_works', blank=True)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


class Review(models.Model):
    volunteer_work = models.ForeignKey(VolunteerWork, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=STAR_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.volunteer_work.title} - {self.user.username} - {self.get_rating_display()}'