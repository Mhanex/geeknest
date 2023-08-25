from django.db import models
from django.contrib.auth.models import AbstractUser


#Create your models here.

class User(AbstractUser):
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to='profile_pictures', default='avatar.jpg', null=True)

    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#Table for all created Room in the Database
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    last_updated = models.DateTimeField(auto_now=True) 
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_updated', '-date_created']

    def __str__(self):
        return self.name
    


# Table for the Message in the Database
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    last_updated = models.DateTimeField(auto_now=True) 
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_updated', '-date_created']

    def __str__(self):
        return self.body[0:20]
