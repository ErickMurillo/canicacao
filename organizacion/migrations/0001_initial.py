# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lugar', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aspectos_Juridicos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tiene_p_juridica', models.IntegerField(verbose_name=b'Personer\xc3\xada jur\xc3\xaddica', choices=[(1, b'Si'), (2, b'No')])),
                ('act_p_juridica', models.IntegerField(verbose_name=b'Actualizaci\xc3\xb3n personer\xc3\xada jur\xc3\xaddica', choices=[(1, b'Si'), (2, b'No')])),
                ('solvencia_tributaria', models.IntegerField(verbose_name=b'Cuenta con solvencia tributaria (DGI)', choices=[(1, b'Si'), (2, b'No')])),
                ('junta_directiva', models.IntegerField(verbose_name=b'Junta Directiva certificada', choices=[(1, b'Si'), (2, b'No')])),
                ('mujeres', models.IntegerField()),
                ('hombres', models.IntegerField()),
                ('lista_socios', models.IntegerField(verbose_name=b'Lista socias/os esta actualizada y certificada', choices=[(1, b'Si'), (2, b'No')])),
                ('ruc', models.CharField(max_length=50, verbose_name=b'No. RUC')),
            ],
            options={
                'verbose_name': 'Aspectos jur\xeddicos',
                'verbose_name_plural': 'Aspectos jur\xeddicos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Datos_Productivos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('socias', models.IntegerField()),
                ('socios', models.IntegerField()),
                ('pre_socias', models.IntegerField()),
                ('pre_socios', models.IntegerField()),
                ('area_total', models.FloatField(verbose_name=b'\xc3\x81rea total establecida por sus socias/os')),
                ('area_cert_organico', models.FloatField(verbose_name=b'\xc3\x81rea con certificado org\xc3\xa1nico')),
                ('area_convencional', models.FloatField(verbose_name=b'\xc3\x81rea convencional')),
                ('cacao_baba', models.FloatField(verbose_name=b'QQ')),
                ('area_cacao_baba', models.FloatField(verbose_name=b'Mz')),
                ('cacao_seco', models.FloatField(verbose_name=b'QQ')),
                ('area_cacao_seco', models.FloatField(verbose_name=b'Mz')),
            ],
            options={
                'verbose_name': 'Datos productivos de la Org. y asociado',
                'verbose_name_plural': 'Datos productivos de la Org. y asociado',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Documentacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documentos', models.IntegerField(choices=[(1, b'Poseen estatutos'), (2, b'Cuentan con plan estrat\xc3\xa9gico'), (3, b'Poseen libro de Actas'), (4, b'Tiene plan de negocios'), (5, b'Cuentan con plan de acopio'), (6, b'Poseen plan de comercializaci\xc3\xb3n')])),
                ('si_no', models.IntegerField(verbose_name=b'Si/No', choices=[(1, b'Si'), (2, b'No')])),
                ('fecha', models.DateField(verbose_name=b'Fecha de elaboraci\xc3\xb3n u actualizaci\xc3\xb3n')),
            ],
            options={
                'verbose_name': 'Inform. sobre documentaci\xf3n en gesti\xf3n',
                'verbose_name_plural': 'Inform. sobre documentaci\xf3n en gesti\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Infraestructura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.IntegerField(verbose_name=b'Tipo de Infraestructura', choices=[(1, b'Centro de Acopio central'), (2, b'Centro de acopio comunitarios'), (3, b'Hornos de secado'), (4, b'Planta de procesamiento'), (5, b'Bodegas'), (6, b'Cuartos fr\xc3\xados'), (7, b'Oficina'), (8, b'Medios de Transporte')])),
                ('cantidad', models.FloatField()),
                ('capacidad', models.FloatField(verbose_name=b'Capacidad de las instalaciones (qq)')),
                ('anno_construccion', models.DateField(verbose_name=b'A\xc3\xb1o de construcci\xc3\xb3n')),
                ('estado', models.IntegerField(verbose_name=b'Estado de infraestructura', choices=[(1, b'Bueno'), (2, b'Malo'), (3, b'Regular')])),
            ],
            options={
                'verbose_name': 'Infraestructura y maquinaria',
                'verbose_name_plural': 'Infraestructura y maquinaria',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200, verbose_name=b'Organizaci\xc3\xb3n/Instituci\xc3\xb3n')),
                ('siglas', models.CharField(max_length=200)),
                ('gerente', models.CharField(max_length=200, verbose_name=b'Director/Gerente')),
                ('status', models.IntegerField(verbose_name=b'Status Legal', choices=[(1, b'------'), (2, b'------')])),
                ('fundacion', models.DateField(verbose_name=b'A\xc3\xb1o fundaci\xc3\xb3n')),
                ('direccion', models.CharField(max_length=300)),
                ('telefono', models.IntegerField(verbose_name=b'N\xc3\xbamero telef\xc3\xb3nico')),
                ('fax', models.IntegerField(verbose_name=b'N\xc3\xbamero fax')),
                ('email', models.EmailField(max_length=75)),
                ('web', models.URLField(verbose_name=b'P\xc3\xa1gina web')),
                ('municipio', models.ForeignKey(to='lugar.Municipio')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Organizaci\xf3n',
                'verbose_name_plural': 'Organizaciones',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='infraestructura',
            name='organizacion',
            field=models.ForeignKey(to='organizacion.Organizacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentacion',
            name='organizacion',
            field=models.ForeignKey(to='organizacion.Organizacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datos_productivos',
            name='organizacion',
            field=models.ForeignKey(to='organizacion.Organizacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aspectos_juridicos',
            name='organizacion',
            field=models.ForeignKey(to='organizacion.Organizacion'),
            preserve_default=True,
        ),
    ]
