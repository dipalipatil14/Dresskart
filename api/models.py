from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager
# from .manager import *


# Create your models here.

class Note(models.Model):
    body = models.TextField()
    original_price=models.TextField()
    price = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Image/', default=True)

    def __str__(self):
        return self.body[0:50]
    
    class Meta:
        ordering = ['-updated']

class UserImage(models.Model):
    image = models.ImageField(upload_to='UserImages/', default=True)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 , null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email must be set')
        
#         user = self.model(email=self.normalize_email(email))
#         user.set_password(password)
#         user.save(using=self.db)
#         return user

# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)
#     is_verified = models.BooleanField(default=False)
#     otp = models.CharField(max_length=6 , null=True, blank=True)

#     objects = UserManager()
#     # objects.create_user(email, password=None)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


#     def __str__(self):
#         return self.email






