# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0005_auto_20150730_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genero',
            name='destino_ingresos_1',
        ),
        migrations.AddField(
            model_name='genero',
            name='destino_ingresos_2',
            field=models.ManyToManyField(to='monitoreo.Destino_Ingresos', null=True, verbose_name=b'Destino de los ingresos percibidos', blank=True),
            preserve_default=True,
        ),
    ]
