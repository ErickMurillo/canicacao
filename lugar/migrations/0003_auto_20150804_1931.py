# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lugar', '0002_auto_20150804_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='latitud_1',
            field=models.FloatField(null=True, verbose_name=b'Latitud', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='departamento',
            name='longitud_1',
            field=models.FloatField(null=True, verbose_name=b'Longitud', blank=True),
            preserve_default=True,
        ),
    ]
