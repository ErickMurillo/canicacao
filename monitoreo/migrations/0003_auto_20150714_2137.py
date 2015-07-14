# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0002_auto_20150707_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizacion_asociada',
            name='socio',
            field=models.IntegerField(default=1, choices=[(1, b'Si'), (2, b'No')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organizacion_asociada',
            name='beneficios',
            field=models.ManyToManyField(to='monitoreo.Beneficios', null=True, verbose_name=b'Beneficios de estar asociado', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizacion_asociada',
            name='organizacion',
            field=models.ManyToManyField(to='organizacion.Organizacion', null=True, verbose_name=b'Organizaci\xc3\xb3n/Instituci\xc3\xb3n con la que trabaja', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizacion_asociada',
            name='tipos_servicio',
            field=models.ManyToManyField(to='monitoreo.Tipos_Servicio', null=True, verbose_name=b'Tipos de servicios que recibe', blank=True),
            preserve_default=True,
        ),
    ]
