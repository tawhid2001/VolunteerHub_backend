from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from VolunteerHub import settings
from django.urls import reverse

# Create your models here.

STAR_CHOICES = [
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.jpg')
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.profile_picture or self.profile_picture == 'default_profile.jpg':
            self.profile_picture = 'default_profile.jpg'
        super().save(*args, **kwargs)


    def send_confirmation_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = settings.SITE_URL + reverse('account_confirm_email', kwargs={'key': f"{uid}:{token}"})
        subject = 'Confirm your email address'
        message = 'Please confirm your email address.'
        html_message = render_to_string('email_confirmation_message.html', {
            'user': user,
            'confirmation_link': confirm_url,
        })
        email = EmailMultiAlternatives(subject, message, '', [user.email])
        email.attach_alternative(html_message, "text/html")
        email.send()

    def send_confirmation_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = settings.SITE_URL + reverse('account_confirm_email', kwargs={'key': f"{uid}:{token}"})
        subject = 'Confirm your email address'
        message = 'Please confirm your email address.'
        html_message = render_to_string('email_confirmation_message.html', {
            'user': user,
            'confirmation_link': confirm_url,
        })
        email = EmailMultiAlternatives(subject,message,'',[user.email])
        email.attach_alternative(html_message,"text/html")
        email.send()
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def __str__(self):
        return self.name

class VolunteerWork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="work_images/",blank=True,null=True)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    organizer = models.ForeignKey(User, related_name='organized_works', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participated_works', blank=True)
    category = models.ForeignKey(Category, related_name='volunteer_works', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.image:
            self.image = "default_image.jpg"
        super().save(*args,**kwargs)

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

    class Meta:
        unique_together = ('volunteer_work', 'user')

    def __str__(self):
        return f'{self.volunteer_work.title} - {self.user.username} - {self.get_rating_display()}'
    

class JoinRequest(models.Model):
    volunteer_work = models.ForeignKey(VolunteerWork, related_name='join_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f'{self.user.username} - {self.volunteer_work.title} ({self.status})'
