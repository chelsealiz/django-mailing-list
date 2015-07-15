# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_mailing_list', '0002_auto_20150622_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='senddata',
            name='store_id',
            field=models.PositiveSmallIntegerField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
