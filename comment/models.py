from django.db import models
from post_framework.models import Post, Thread


class Comment(Post, models.Model):
	
    parent = models.ForeignKey(Thread, blank=False, null=False)
    text = models.CharField(null=False, max_length=300)

    def detail(self):
        return u'%s' % self.text

    def css_class(self):
        return "comment-type"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        #ordering = ['added_at']
