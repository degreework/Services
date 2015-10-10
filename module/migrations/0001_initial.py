# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum_wrap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ask', models.ForeignKey(to='forum.Ask')),
            ],
            options={
                'verbose_name': 'Forum_wrap',
                'verbose_name_plural': 'Forum_wraps',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
            },
        ),
        migrations.AddField(
            model_name='forum_wrap',
            name='module',
            field=models.ForeignKey(to='module.Module'),
        ),
    ]
