from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Create your models here.
from django.db import models


from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField(default = 0)
    dob = models.DateField()
    gender = models.IntegerField(default = 0)
    is_active = models.BooleanField(default = False)
    last_login = None
    is_superuser = models.BooleanField(default = True)
    first_name = None
    last_name = None
    objects = CustomUserManager()
    is_staff = models.BooleanField(default = True)



