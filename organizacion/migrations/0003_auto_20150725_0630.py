# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0002_auto_20150723_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='comercializacion_org',
            name='fecha',
            field=models.IntegerField(default=1, verbose_name=b'A\xc3\xb1o de recolecci\xc3\xb3n de informaci\xc3\xb3n'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organizacion',
            name='gerente',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Representante legal', blank=True),
            preserve_default=True,
        ),
    ]
