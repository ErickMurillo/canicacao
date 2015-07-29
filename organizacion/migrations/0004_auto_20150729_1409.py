# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizacion', '0003_auto_20150725_0630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta_Org',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('anno', models.IntegerField()),
                ('organizacion', models.ForeignKey(related_name='Organizacion', to='organizacion.Organizacion')),
                ('usuario', models.ForeignKey(related_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Encuesta',
                'verbose_name_plural': 'Encuestas',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='acopio_comercio',
            name='organizacion',
        ),
        migrations.RemoveField(
            model_name='aspectos_juridicos',
            name='organizacion',
        ),
        migrations.RemoveField(
            model_name='comercializacion_importancia',
            name='organizacion',
        ),
        migrations.RemoveField(
            model_name='comercializacion_org',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='comercializacion_org',
            name='organizacion',
        ),
        migrations.RemoveField(
            model_name='datos_productivos',
            name='organizacion',
        ),
        migrations.RemoveField(
            model_name='documentacion',
            name='organizacion',
        ),
        migrations.RemoveField(
            model_name='infraestructura',
            name='organizacion',
        ),
        migrations.RemoveField(
            model_name='organizacion',
            name='usuario',
        ),
        migrations.AddField(
            model_name='acopio_comercio',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='organizacion.Encuesta_Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aspectos_juridicos',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='organizacion.Encuesta_Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comercializacion_importancia',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='organizacion.Encuesta_Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comercializacion_org',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='organizacion.Encuesta_Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datos_productivos',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='organizacion.Encuesta_Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentacion',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='organizacion.Encuesta_Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infraestructura',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='organizacion.Encuesta_Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizacion',
            name='tipo',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Tipo de Organizaci\xc3\xb3n', choices=[(1, b'Miembro Canicacao'), (1, b'Organizaci\xc3\xb3n de apoyo')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='acopio_comercio',
            name='seleccion',
            field=multiselectfield.db.fields.MultiSelectField(max_length=7, choices=[(1, b'Propio'), (2, b'Cr\xc3\xa9dito bancario'), (3, b'Cooperaci\xc3\xb3n Internacional'), (4, b'Financiamiento del comprador')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aspectos_juridicos',
            name='hombres',
            field=models.IntegerField(verbose_name=b'Miembros hombres JD'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aspectos_juridicos',
            name='mujeres',
            field=models.IntegerField(verbose_name=b'Miembros mujeres JD'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializacion_org',
            name='destino_produccion',
            field=multiselectfield.db.fields.MultiSelectField(max_length=5, choices=[(1, b'Mercado Local'), (2, b'Mercado Nacional'), (3, b'Mercado Internacional')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializacion_org',
            name='tipo_mercado',
            field=multiselectfield.db.fields.MultiSelectField(max_length=7, choices=[(1, b'Convencional'), (2, b'Org\xc3\xa1nico'), (3, b'Comercio Justo'), (4, b'UTZ')]),
            preserve_default=True,
        ),
    ]
