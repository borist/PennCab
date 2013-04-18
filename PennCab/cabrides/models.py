import datetime

from django.db import models
from django.utils import timezone
"""
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

def MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, email, password=None, photo)

    if not email or if not phone_number:
        raise ValueError('User must have email and phon number')

    user = self.model(
       
""" 

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, default="###-###-####")
    email = models.EmailField(max_length=200, default="example@upenn.edu")
    password = models.CharField(max_length=20)
    photo = models.URLField()

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Ride(models.Model):
    ride_owner = models.ForeignKey(User, related_name="owner_of")
    participants = models.ManyToManyField(User)
    ride_date = models.DateTimeField('Time and Date of Ride')
    max_riders = models.IntegerField(default=4)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    purpose = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return "Ride to: %s, owned by %s" % (self.destination, self.ride_owner)

    def num_available_spots(self):
        num = self.max_riders - self.participants.count()
        if num <= 0:
            return None
        else:
            return range(num)

    def ride_in_past(self):
        return self.ride_date < timezone.now()

