import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, email, password=None):
        if not email or not phone_number:
            raise ValueError('Users must have an email adress and a phone number')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            email = MyUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, email, password):
        user = self.create_user(first_name,
            last_name,
            phone_number,
            email,
            password)   
        user.is_admin = True
        user.save(using=self._db)
        return user


class CabUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, default="###-###-####")
    email = models.EmailField(max_length=200, 
        default='example@upenn.edu',
        verbose_name='email address',
        unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def is_staff(self):
        return True #self.is_admin


class Ride(models.Model):
    ride_owner = models.ForeignKey(CabUser, related_name="owner_of")
    participants = models.ManyToManyField(CabUser)
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

