from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete = models.CASCADE)

    #additional classes
    portfolio_site = models.URLField(blank = True) # blank = True allows user to leave this field blank without returning an error
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True)

    def __str__(self):
        return self.user.username
