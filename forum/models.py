from django.db import models

from post_framework.models import Post, Thread


class Ask(Thread, Post, models.Model):
    title = models.CharField(null=False, max_length=300)
    text = models.TextField(null=False)

    def __str__(self):
        return u'%s - %s' % (self.id, self.title)

    class Meta:
        verbose_name = "Ask"
        verbose_name_plural = "Asks"


class Answer(Thread, Post, models.Model):
    ask = models.ForeignKey(Ask, related_name='answers_Answer')
    text = models.TextField(null=False)
    
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        #ordering = ['added_at']

    def __str__(self):
        return u'%s - %s' % (self.id, self.ask)