# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comunidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Comunidades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.IntegerField(serialize=False, verbose_name=b'C\xc3\xb3digo', primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('slug', models.SlugField(help_text=b'Usado como url unica(autorellenado)', unique=True, null=True)),
                ('extension', models.DecimalField(null=True, verbose_name=b'Extension Territorials', max_digits=10, decimal_places=2, blank=True)),
                ('latitud', models.DecimalField(null=True, verbose_name=b'Latitud', max_digits=8, decimal_places=5, blank=True)),
                ('longitud', models.DecimalField(null=True, verbose_name=b'Longitud', max_digits=8, decimal_places=5, blank=True)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Departamentos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.IntegerField(serialize=False, verbose_name=b'C\xc3\xb3digo', primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('slug', models.SlugField(help_text=b'Usado como url unica(autorellenado)', unique=True, null=True)),
                ('extension', models.DecimalField(null=True, verbose_name=b'Extension Territorial', max_digits=10, decimal_places=2, blank=True)),
                ('latitud', models.DecimalField(null=True, verbose_name=b'Latitud', max_digits=8, decimal_places=5, blank=True)),
                ('longitud', models.DecimalField(null=True, verbose_name=b'Longitud', max_digits=8, decimal_places=5, blank=True)),
                ('departamento', models.ForeignKey(to='lugar.Departamento')),
            ],
            options={
                'ordering': ['departamento__nombre', 'nombre'],
                'verbose_name_plural': 'Municipios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('codigo', models.CharField(help_text=b'C\xc3\xb3digo de 2 letras del pa\xc3\xads, ejemplo : Nicaragua (ni)', max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Pa\xedses',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='departamento',
            name='pais',
            field=models.ForeignKey(to='lugar.Pais'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comunidad',
            name='municipio',
            field=models.ForeignKey(to='lugar.Municipio'),
            preserve_default=True,
        ),
    ]
