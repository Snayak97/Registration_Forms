from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    adress=models.TextField()
    profile_pic=models.ImageField()