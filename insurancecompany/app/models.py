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

class Client(models.Model):
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    aadhar = models.CharField(max_length=12, null=True, blank=True)
    pan = models.CharField(max_length=10, null=True, blank=True)
    income_level = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], null=True, blank=True)
    children = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    source = models.JSONField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    claim_satisfaction = models.IntegerField(null=True, blank=True)
    insurance_area = models.JSONField(null=True, blank=True)
    agent_visited_policy = models.FileField(upload_to='uploads/', null=True, blank=True)
    willingness_to_purchase = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    willingness_to_share_previous_insurance = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    customer_preferences = models.TextField(null=True, blank=True)
    agent_notes = models.TextField(null=True, blank=True)
    willingness_to_switch = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], null=True, blank=True)
    existing_profile_details = models.FileField(upload_to='uploads/', null=True, blank=True)

   



    