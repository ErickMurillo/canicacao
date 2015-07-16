# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0002_auto_20150715_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educacion',
            name='bachiller',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='no_lee_ni_escribe',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='numero_total',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='primaria_completa',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='primaria_incompleta',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='rango',
            field=models.IntegerField(default=1, verbose_name=b'Selecci\xc3\xb3n', choices=[(1, b'Hombres mayores 31 a\xc3\xb1os'), (2, b'Mujeres mayores 31 a\xc3\xb1os'), (3, b'Hombre joven 19 a 30 a\xc3\xb1os'), (4, b'Mujer joven 19 a 30 a\xc3\xb1os'), (5, b'Hombre adoles. 13 a 18 a\xc3\xb1os'), (6, b'Mujer adoles. 13 a 18 a\xc3\xb1os'), (7, b'Ni\xc3\xb1os 0 a 12 a\xc3\xb1os'), (8, b'Ni\xc3\xb1as 0 a 12 a\xc3\xb1os'), (9, b'Ancianos (> 64 a\xc3\xb1os)')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='secundaria_incompleta',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='universitario_tecnico',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educacion',
            name='viven_fuera',
            field=models.IntegerField(default=1, verbose_name=b'N\xc3\xbamero de personas que viven fuera de la finca'),
            preserve_default=False,
        ),
    ]
