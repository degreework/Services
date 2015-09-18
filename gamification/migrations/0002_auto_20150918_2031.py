# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scores',
            name='activity_score',
        ),
        migrations.RemoveField(
            model_name='scores',
            name='quiz_score',
        ),
        migrations.RemoveField(
            model_name='scores',
            name='wiki_score',
        ),
        migrations.AddField(
            model_name='scores',
            name='event',
            field=models.CharField(default=b'wiki', help_text=b'', max_length=30, verbose_name='Event Order', choices=[(b'Wiki', 'Wiki'), (b'Quiz', 'Quiz'), (b'Activity', 'Activity')]),
        ),
        migrations.AddField(
            model_name='scores',
            name='id_event',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='scores',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
