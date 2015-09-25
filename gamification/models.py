# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

EVENT_ORDER_OPTIONS = (
    ('Wiki', _('Wiki')),
    ('Quiz', _('Quiz')),
    ('Activity', _('Activity'))
)


class Scores(models.Model):
    

    event = models.CharField(
        default = ' ',
        max_length=30, 
        choices = EVENT_ORDER_OPTIONS,
        help_text=_(""),
        verbose_name=_("Event Order"))

    id_event = models.PositiveIntegerField(blank=True, default= 0)
    score = models.PositiveIntegerField(null=False, default= 0)
    
    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"


"""Votes for Ask, Answers"""
from django.conf import settings
from django.core.exceptions import PermissionDenied

from post_framework.models import Thread

class Votes(models.Model):

    VOTES = (
        (0, "up"),
        (1, "down"),
        )
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    vote = models.CharField(max_length=1, choices=VOTES)

    @classmethod
    def create(cls, thread, author, vote, *args, **kwargs):
        antecedents = Votes.objects.filter(thread=thread, author=author)
        if antecedents:
            if 1 == len(antecedents):
                if int(antecedents[0].vote[0]) != vote:
                    antecedents[0].vote = vote
                    antecedents[0].save()
                    return antecedents[0]
        else:
            vote = cls(thread=thread, author=author, vote=vote)
            vote.save()
            return vote

        raise PermissionDenied



    class Meta:
        verbose_name = "Votes"
        verbose_name_plural = "Votes"

    def __str__(self):
        return u"%s - %s" % (self.thread, Votes.VOTES[int(self.vote[0])][1])
    
