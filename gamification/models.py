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
