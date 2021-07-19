# from django.db import models
from djongo import models

# Create your models here.

class SocialLinks(models.Model):
    twitter = models.CharField(max_length=200)
    facebook = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200)