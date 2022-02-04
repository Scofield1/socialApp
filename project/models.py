from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField()
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile')

    def __str__(self):
        return self.user.username


class TopicModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class RoomModel(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(TopicModel, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='participants')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.topic.name


class MessageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated', '-created']

