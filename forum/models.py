from django.db import models

from post_framework.models import Post


class Ask(Post, models.Model):
    title = models.CharField(null=False, max_length=300)
    text = models.TextField(null=False)

    class Meta:
        verbose_name = "Ask"
        verbose_name_plural = "Asks"



class Answer(Post, models.Model):
    ask = models.ForeignKey(Ask, related_name='answers_Answer')
    text = models.TextField(null=False)
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"   