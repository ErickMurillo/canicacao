# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0004_auto_20150728_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destino_Ingresos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Destino de ingresos percibidos',
                'verbose_name_plural': 'Destino de ingresos percibidos',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='genero',
            name='destino_ingresos',
        ),
        migrations.AddField(
            model_name='genero',
            name='destino_ingresos_1',
            field=models.ForeignKey(verbose_name=b'Destino de los ingresos percibidos', blank=True, to='monitoreo.Destino_Ingresos', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adicional',
            name='cuanto',
            field=models.FloatField(default=b'0', null=True, verbose_name=b'Cuanto (Mz)', blank=True),
            preserve_default=True,
        ),
    ]
