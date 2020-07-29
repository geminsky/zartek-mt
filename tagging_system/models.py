from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=20, null=True, unique=False)
    weightage = models.IntegerField(null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Images(models.Model):
    image = models.ImageField(null=True)
    description = models.TextField(null=True)
    tag = models.ManyToManyField(Tags, null=True)
    likes = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ImageStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_liked = models.BooleanField(default=False)
    image = models.ForeignKey(Images, on_delete=models.CASCADE, null=True)