from django.db import models

class UserProfile(models.Model):
    """
    Each User within the post service is represented by this
    class.

    This user model(table) is a replicate of the user table in user service
    """
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    first_name = models.CharField(verbose_name='first name', max_length=150)
    last_name = models.CharField(verbose_name='last name', max_length=150)
    email = models.EmailField(verbose_name='email address')
    avatar = models.CharField(verbose_name='profile photo', max_length=500)
    phone = models.CharField(verbose_name='phone', max_length=15)
    role = models.IntegerField(verbose_name='role', default=0)
    createdAt = models.DateTimeField(verbose_name="createdAt", auto_now_add=True)
    updatedAt = models.DateTimeField(verbose_name="updatedAt", auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-createdAt']
