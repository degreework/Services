# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waliki', '0006_auto_20150729_0209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commit', models.CharField(max_length=7)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(to='waliki.Page')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
        ),
    ]
