# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_mailing_list', '0003_senddata_store_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SendData',
        ),
    ]
