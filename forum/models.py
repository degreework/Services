from django.db import models

from post_framework.models import Post


class Ask(Post, models.Model):
    title = models.CharField(null=False, max_length=300)

    class Meta:
        verbose_name = "Ask"
        verbose_name_plural = "Asks"
        db_table = 'ask_post'



class Answer(Post, models.Model):
    ask = models.ForeignKey(Ask, related_name='answers_Answer')
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        db_table = 'answer_post'       