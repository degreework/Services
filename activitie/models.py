# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import PermissionDenied

from django.conf import settings

from post_framework.models import Thread

from django.utils import timezone
from django.utils.translation import ugettext as _

class ActivitieParent(Thread):
    """
    This model define a Activite created by a Teacher
    """
    die_at = models.DateTimeField()

    name = models.CharField(_(u'Nombre'), max_length=50)
    description = models.TextField(_(u'Descripción'))

    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return ("%s" % self.name)

    def detail(self):
        return u'%s' % self.name

    def css_class(self):
        return "activitie-p-type"

    class Meta:
        verbose_name = "ActivitieParent"
        verbose_name_plural = "ActivitieParents"
        permissions = (("can_view", "Can view Activitie"),)


class ActivitieChild(models.Model):
    """
    This model define a Activite sent by a Student in response to ActiviteParent
    """

    def generate_filename(instance, filename):
        #generate new path
        out_file = unicode( instance.id) +"."+ unicode( filename.split(".")[-1] )
        
        path = '/'.join([instance.author.generate_folder_path(), 'activities', str(instance.parent.pk) , out_file])
        return path

    STATUS = (
        (0, 'No enviado'),
        (1, 'Enviado'),
        (2, 'En revisión'),
        (3, 'Aprobado'),
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

    def save(self, *args, **kwargs):
        now = timezone.now()
        die_at = self.parent.die_at

        delta = die_at - now
        
        if delta.total_seconds() > 0:
            super(ActivitieChild, self).save(*args, **kwargs)
        else:
            raise PermissionDenied
            
