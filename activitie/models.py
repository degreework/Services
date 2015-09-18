# -*- coding: utf-8 -*-
from django.db import models

from django.conf import settings


from post_framework.models import Thread


import datetime
from django.utils import timezone
from django.utils.timezone import utc


class ActivitieParent(Thread):
    die_at = models.DateTimeField()

    name = models.CharField(max_length=50)
    description = models.TextField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return ("%s" % self.name)

    class Meta:
        verbose_name = "ActivitieParent"
        verbose_name_plural = "ActivitieParents"


class ActivitieChild(models.Model):
    def generate_filename(instance, filename):
        #generate new path
        out_file = unicode( instance.id) +"."+ unicode( filename.split(".")[-1] )
        
        path = '/'.join([instance.author.generate_folder_path(), 'activities', str(instance.parent.pk) , out_file])
        return path

    STATUS = (
        (0, 'No enviado'),
        (1, 'Enviado'),
        (2, 'En revisión'),
        (3, 'Aprovado'),
        (4, 'Rechazado'),
    )

    parent = models.ForeignKey(ActivitieParent)

    sent_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=generate_filename)
    status = models.CharField(max_length=1, choices=STATUS, default=1)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = "ActivitieChild"
        verbose_name_plural = "ActivitieChilds"
        permissions = (("can_check_activitie", "Can check activities"),)

    def __str__(self):
        return ("%s - %s" % (self.parent.name, self.author))

    def do_approved(self, checked_by):
        self.status = 3
        self.save()
        return True

    def do_rejected(self, checked_by):
        self.status = 4
        self.save()
        return True
"""
    def save(self, *args, **kwargs):
        print("save")

        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        die_at = self.parent.die_at

        delta = die_at - now

        if delta.total_seconds() > 0:
            print("ok")
        else:
            print("late")
            
            raise SomeException("Too late")
            

        #super(ActivitieChild).objects.create(author=user, parent=parent_activitie, file=validated_data['file'])

"""