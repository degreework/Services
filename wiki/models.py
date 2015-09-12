from django.db import models

from users.models import User
from waliki.models import Page
from post_framework.models import Thread

import datetime


class Request(models.Model):
    """
    Represent change request from a user
    """
    page = models.ForeignKey(Page)
    commit = models.CharField(max_length=7)

    checked = models.BooleanField(default=False)

    approved = models.BooleanField(default=False, db_index=True)
    checked_by = models.ForeignKey(User, null=True, blank=True, related_name="reviewer")
    checked_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name="author")

    def __str__(self):
        return u'%s' % (self.commit, )

    def approve_request(self, user):
        self.checked = True
        self.approved = True
        self.checked_by = user
        self.checked_at = datetime.datetime.now()
        self.save()
        PublicPage.objects.filter(request__page=self.page).delete()
        PublicPage(request=self).save()
        return True

    def reject_request(self, user):
        self.checked = True
        self.checked_by = user
        self.checked_at = datetime.datetime.now()
        self.save()
        return True
    
    
    class Meta:
        #app_label = 'waliki'
        #db_table = 'wiki_request'
        verbose_name = "Request"
        verbose_name_plural = "Requests"
        permissions = (("can_approve_request", "Can approve requests"),)


class pageComments(Thread, models.Model):
    page = models.ForeignKey(Page)


class PublicPage(models.Model):
    """
    Contains all Published wiki Pages
    """
    request = models.ForeignKey(Request)

