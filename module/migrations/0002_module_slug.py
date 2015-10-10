# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 10, 7, 21, 44, 20, 803511, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
