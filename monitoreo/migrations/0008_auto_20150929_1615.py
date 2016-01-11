# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0007_auto_20150731_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='uso_tierra',
            name='cafe',
            field=models.FloatField(default=b'0', verbose_name=b'Caf\xc3\xa9', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='area_pasto_abierto',
            field=models.FloatField(default=b'0', verbose_name=b'\xc3\x81rea de pastos abierto', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='area_pasto_arboles',
            field=models.FloatField(default=b'0', verbose_name=b'\xc3\x81rea de pastos con \xc3\xa1rboles', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='area_total',
            field=models.FloatField(default=b'0', verbose_name=b'\xc3\x81rea total en manzanas de la propiedad', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='bosque',
            field=models.FloatField(default=b'0', verbose_name=b'Bosques', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='cacao',
            field=models.FloatField(default=b'0', verbose_name=b'Solo destinado para cacao', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='cultivo_anual',
            field=models.FloatField(default=b'0', verbose_name=b'Cultivo anual ( que produce en el a\xc3\xb1o)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='cultivo_perenne',
            field=models.FloatField(default=b'0', verbose_name=b'Cultivo perenne (frutales)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='cultivo_semi_perenne',
            field=models.FloatField(default=b'0', verbose_name=b'Cultivo semi-perenne (mus\xc3\xa1cea, pi\xc3\xb1a)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='huerto_mixto_cacao',
            field=models.FloatField(default=b'0', verbose_name=b'Huerto mixto con cacao', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='otros',
            field=models.FloatField(default=b'0', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='plantacion_forestal',
            field=models.FloatField(default=b'0', verbose_name=b'Plantaci\xc3\xb3n forestal ( madera y le\xc3\xb1a)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uso_tierra',
            name='tacotal',
            field=models.FloatField(default=b'0', verbose_name=b'Tacotal o \xc3\xa1rea de descanso', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
    ]
