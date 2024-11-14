from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, null=True)
    place = models.CharField(max_length=25, null=True)
    image = models.ImageField(upload_to='agents/', null=True)

class Campaign(models.Model):
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    location = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='campaigns/', null=True)


    