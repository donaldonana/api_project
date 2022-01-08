from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, email, last_name, phone, password=None):
        """create the new user profile"""
        if not email:
            raise ValueError("User most have a email")

        # email = self.normalize_email(email)
        user = self.model(email=email, last_name=last_name, phone = phone)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, last_name, phone, password):
        """create and save superuser with given detail"""
        user = self.create_user(email, last_name, phone, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin, models.Model):

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True)
    # avatar = models.CharField(max_length = 255, blank = True)
    # avatar = models.FileField(upload_to="images/%Y/%m/%d", blank=True, null=True)
    # settings = JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["last_name", "phone"]

    def get_last_name(self):

    	return self.last_name

    