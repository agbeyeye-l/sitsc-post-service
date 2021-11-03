from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from users.models import UserProfile


class Post(models.Model):
    """
    Posts describe User-generated content—such as text 
    or comments, digital photos or videos, and 
    data generated through all interactions on SIT-SC platform.
    """
    title = models.CharField( verbose_name= "title", max_length = 300, blank= True, null= True,
        help_text=('Designates the title of a post'))
    body = models.TextField( verbose_name="body", blank= True, null= True, help_text=('Designates the body of a post'))
    picture = models.CharField( verbose_name="image", max_length= 300, blank= True, null= True,
        help_text=('Designates an image of a post'))
    isAnonymous = models.BooleanField(default = False, help_text=('Designates if the owner wants to remain anonymous or not'))
    isSuspended = models.BooleanField(default= False,help_text=('Designates if a post is banned or not'))
    createdBy = models.ForeignKey(UserProfile, on_delete= models.CASCADE, help_text=('Designates the owner of a post'))
    updatedAt = models.DateTimeField(verbose_name="updatedAt",auto_now=True)
    createdAt = models.DateTimeField(verbose_name="createdAt", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering =['-createdAt']


class Comment(models.Model):
    """
    Comment class represents messages that people leave in response to a post made on
    the SIT-SC platform
    """
    body = models.CharField(max_length=500,help_text=('The content of a comment on a post'))
    createdBy = models.ForeignKey(UserProfile, on_delete= models.CASCADE,help_text=('Designates the owner of the comment'))
    createdAt = models.DateTimeField(verbose_name="createdAt", auto_now_add=True, help_text=('Time comment is created'))
    updatedAt = models.DateTimeField(verbose_name="updatedAt",auto_now=True,help_text=('Time comment is updated'))
    post = models.ForeignKey(Post, on_delete= models.CASCADE,help_text=('The post to which the comment belong'))

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-createdAt']
