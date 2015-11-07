# -*- coding: utf-8 -*-
"""This file provide classes to model a User in app"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from degree.models import Degree

import os
from easy_thumbnails.fields import ThumbnailerImageField

from project.settings import MEDIA_ROOT
from django.conf import settings
from project.settings import REGISTRATION_DEFAULT_GROUP_NAME
from django.contrib.auth.models import Group


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, codigo, first_name, last_name,
                    password, is_superuser=False, plan=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        #now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                        first_name=first_name,
                        last_name=last_name,
                        codigo=codigo,
                        is_superuser=is_superuser,
                        plan=plan,
                        **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, codigo, first_name, last_name, password=None, plan=None, **extra_fields):
        user = self._create_user(email, codigo, first_name, last_name, password, False, plan,
                                 **extra_fields)

        for GROUP in REGISTRATION_DEFAULT_GROUP_NAME:
            user.groups.add(Group.objects.get(name=GROUP))
        return user

    def create_superuser(self, email, codigo, first_name, last_name, password, **extra_fields):
        return self._create_user( email, codigo, first_name, last_name, password, True,
                                 **extra_fields)

#Anexo 1
class User(AbstractBaseUser, PermissionsMixin):
    """
    Class User, define a user
    """ 
    def _content_file_name(instance, filename):
        #generate new path
        out_file = unicode( instance.id) +"."+ unicode( filename.split(".")[-1] )
        path = '/'.join([instance.generate_folder_path(), 'photos',  out_file])

        #remove current files (photos)
        ### WARNING ####
        #this way is not secure, but easy-thumbnails 2.2 not have a functional delete method
        try:
            
            old_path = MEDIA_ROOT + path
            print old_path
            
            dir = os.path.dirname(old_path) + '/'     
            if os.path.exists(dir):
                for f in os.listdir(dir):
                    file = dir + f
                    os.remove(file)
        except Exception(e):
            print(e)
        # end remove
        
        return path


    photo = ThumbnailerImageField(upload_to=_content_file_name, resize_source=settings.DEFAULT_USER_IMAGE_SETTING, blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)


    codigo = models.IntegerField(blank=False, unique=True)
    plan = models.ForeignKey(Degree, null=True, blank=True)

    email = models.EmailField(unique=True)
    

    is_active = models.BooleanField(default=True)
    #is_staff  = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now=True)


    objects = UserManager()


    #field for login
    USERNAME_FIELD = 'email'

    #requires this fields
    REQUIRED_FIELDS = ['first_name', 'last_name', 'codigo']


    @property
    def username(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_superuser
    

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.__str__()

    def generate_folder_path(self):
        return (u'u_%s' % (self.id))

    class Meta:
        #app_label = 'users'
        swappable = 'AUTH_USER_MODEL'
        permissions = (("can_view", "Can view Users"),("can_list", "Can list Users"))
