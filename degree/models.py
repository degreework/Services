# -*- coding: utf-8 -*-
from django.db import models

class Degree(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(null=False, max_length=50)

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.name)
    