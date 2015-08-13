# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_mailing_list', '0004_delete_senddata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='mailing_lists',
            field=models.ManyToManyField(to='google_mailing_list.MailingList', blank=True),
        ),
    ]
