from django.db import models

from waliki.models import Page


class Request(models.Model):
    """
    ""Represent change request from a user
    """
    page = models.ForeignKey(Page)
    commit = models.CharField(max_length=7)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'%s' % (self.commit, )
    
    class Meta:
        #app_label = 'waliki'
        #db_table = 'wiki_request'
        verbose_name = "Request"
        verbose_name_plural = "Requests"

