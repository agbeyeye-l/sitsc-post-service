from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from users.models import UserProfile

class Gallery(models.Model):
    """
    This class represents gallery object
    """
    images = ArrayField(models.TextField(), help_text=('Images of a gallery'))
    tag = models.CharField(max_length=200, help_text=('Describes the name of a gallery by which user can search'))
    createdBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE, help_text=('Designates the creator of a gallery'))
    createdAt = models.DateTimeField(auto_now_add=True, help_text=('Designates the time of creation of a gallery'))
    updatedAt = models.DateTimeField(auto_now=True, help_text=('Designates the time of update of a gallery'))

    class Meta:
        ordering = ['-createdAt']

    def __str__(self):
        return self.tag
