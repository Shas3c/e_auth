#from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User

#Create Your Models Here

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

def __str__(self):
    return self.user.username

    