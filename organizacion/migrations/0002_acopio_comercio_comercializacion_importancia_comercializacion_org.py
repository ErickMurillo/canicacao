# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acopio_Comercio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seleccion', models.IntegerField(choices=[(1, b'Propio'), (2, b'Cr\xc3\xa9dito bancario'), (3, b'Cooperaci\xc3\xb3n Internacional'), (4, b'Financiamiento del comprador')])),
                ('organizacion', models.ForeignKey(to='organizacion.Organizacion')),
            ],
            options={
                'verbose_name': 'Financiamiento de acopio y comerc.',
                'verbose_name_plural': 'Financiamiento de acopio y comerc.',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comercializacion_Importancia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orden_importancia', models.CharField(max_length=200, verbose_name=b'Donde comercializa su cacao (por orden de importancia)')),
                ('organizacion', models.ForeignKey(to='organizacion.Organizacion')),
            ],
            options={
                'verbose_name': 'Comercializaci\xf3n Cacao',
                'verbose_name_plural': 'Comercializaci\xf3n Cacao',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comercializacion_Org',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cacao_baba_acopiado', models.FloatField(verbose_name=b'Cacao en baba acopiado (qq)')),
                ('cacao_seco_comercializado', models.FloatField(verbose_name=b'Cacao en seco comercializado (qq)')),
                ('socios_cacao', models.IntegerField(verbose_name=b'Socios que entregaron cacao al acopio')),
                ('productores_no_asociados', models.IntegerField(verbose_name=b'Productores no asociados')),
                ('tipo_producto', models.IntegerField(verbose_name=b'Tipo de producto comercializado', choices=[(1, b'Caco rojo'), (2, b'Cacao fermentado'), (3, b'Ambos')])),
                ('tipo_mercado', models.IntegerField(choices=[(1, b'Convencional'), (2, b'Org\xc3\xa1nico'), (3, b'Comercio Justo'), (4, b'UTZ')])),
                ('destino_produccion', models.IntegerField(choices=[(1, b'Mercado Local'), (2, b'Mercado Nacional'), (3, b'Mercado Internacional')])),
                ('organizacion', models.ForeignKey(to='organizacion.Organizacion')),
            ],
            options={
                'verbose_name': 'Comercializaci\xf3n de la Organizaci\xf3n',
                'verbose_name_plural': 'Comercializaci\xf3n de la Organizaci\xf3n',
            },
            bases=(models.Model,),
        ),
    ]
