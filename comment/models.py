from django.db import models
from post_framework.models import Post


class Comment(Post, models.Model):
	
    #parent = models.ForeignKey(Ask, blank=True, null=True, related_name='comments') # Answer or Question for Comment
    text = models.CharField(null=False, max_length=300)
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        #ordering = ['added_at']
