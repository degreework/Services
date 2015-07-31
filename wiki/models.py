from django.db import models

from users.models import User
from waliki.models import Page


class Request(models.Model):
    """
    Represent change request from a user
    """
    page = models.ForeignKey(Page)
    commit = models.CharField(max_length=7)

    approved = models.BooleanField(default=False, db_index=True)
    approved_by = models.ForeignKey(User, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'%s' % (self.commit, )

    def approve_request(self, user):
        self.approved = True
        self.approved_by = user
        self.save()
        return True
    
    class Meta:
        #app_label = 'waliki'
        #db_table = 'wiki_request'
        verbose_name = "Request"
        verbose_name_plural = "Requests"
