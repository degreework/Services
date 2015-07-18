# -*- coding: utf-8 -*-
"""This file provide classes to model a User in app"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#from django.utils import timezone
from degree.models import Degree

class UserManager(BaseUserManager):
    """
    This class improbe methods for create users and superusers
    """
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        #now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          #date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        create a user
        """
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """used to create a superuser"""
        return self._create_user(email, password, True, True,
                                 **extra_fields)


from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings

#Anexo 1
class User(AbstractBaseUser, PermissionsMixin):
    """
    Class User, define a user
    """ 
    def content_file_name(instance, filename):
        out_file = unicode( instance.id) +"."+ unicode( filename.split(".")[-1] )
        return '/'.join(['photos', u'%s' % (instance.id), out_file])



    #Codes are Hardcoded, this shouldn't be so
    PLAN_TEC = 2222
    PLAN_ING = 3743
    #

    PLAN_CHOICES = (
        (PLAN_TEC, str('Tecnología de sistemas')),
        (PLAN_ING, str('Ingeniería de sistemas')),
    )

    photo = ThumbnailerImageField(upload_to=content_file_name, resize_source=settings.DEFAULT_USER_IMAGE_SETTING, blank=True)
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)


    codigo = models.IntegerField(blank=False, unique=True)
    plan = models.ForeignKey(Degree, null=True)

    email = models.EmailField(unique=True)
    

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()


    #field for login
    USERNAME_FIELD = 'email'

    #requires this fields
    REQUIRED_FIELDS = ['first_name', 'last_name', 'codigo']


    def __str__(self):
        return u'%s : %s %s' % (self.codigo, self.first_name, self.last_name)

    def get_short_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_full_name(self):
        return self.__str__()

    @property
    def username(self):
        return self.email

    class Meta:
        app_label = 'users'