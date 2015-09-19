# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quiz_score', models.PositiveIntegerField()),
                ('wiki_score', models.PositiveIntegerField()),
                ('activity_score', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Score',
                'verbose_name_plural': 'Scores',
            },
        ),
    ]
