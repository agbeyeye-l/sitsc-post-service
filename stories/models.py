from django.db import models
from users.models import UserProfile
from django.utils import timezone

class Story(models.Model):
    """
    Story class represent success stories shared by users on the platform
    """
    title = models.CharField( verbose_name= "title", max_length = 300)
    body = models.TextField( verbose_name="body")
    image = models.CharField( verbose_name="image", max_length= 300, blank= True, null= True)
    isAnonymous = models.BooleanField(default = False)
    isSuspended = models.BooleanField(default= False)
    isFeatured = models.BooleanField(default= False)
    createdBy = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    createdAt = models.DateTimeField(verbose_name="createdAt", auto_now_add=True)
    updatedAt = models.DateTimeField(verbose_name="updatedAt", auto_now=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-createdAt']
