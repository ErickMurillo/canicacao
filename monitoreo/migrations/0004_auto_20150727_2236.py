# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0003_auto_20150725_0653'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'verbose_name': 'Persona encuestada', 'verbose_name_plural': 'Personas encuestadas'},
        ),
    ]
