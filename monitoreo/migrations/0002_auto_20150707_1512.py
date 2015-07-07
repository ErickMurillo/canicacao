# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizacion', '0001_initial'),
        ('lugar', '__first__'),
        ('monitoreo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizacion_asociada',
            name='organizacion',
            field=models.ManyToManyField(to='organizacion.Organizacion', verbose_name=b'Organizaci\xc3\xb3n/Instituci\xc3\xb3n con la que trabaja'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizacion_asociada',
            name='tipos_servicio',
            field=models.ManyToManyField(to='monitoreo.Tipos_Servicio', verbose_name=b'Tipos de servicios que recibe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mitigacion_riesgos',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inversion',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genero_2',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genero',
            name='actividades',
            field=models.ManyToManyField(to='monitoreo.Actividades_Produccion', verbose_name=b'Actividades en las que participa'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genero',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fenomenos_naturales',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='familia',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuesta',
            name='organizacion',
            field=models.ForeignKey(verbose_name=b'Organizaci\xc3\xb3n', to='organizacion.Organizacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuesta',
            name='persona',
            field=models.ForeignKey(verbose_name=b'Nombre', to='monitoreo.Persona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuesta',
            name='recolector',
            field=models.ForeignKey(to='monitoreo.Recolector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuesta',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='educacion',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='distancia_comercio_cacao',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comercializacion_cacao',
            name='donde_vende',
            field=models.ManyToManyField(to='lugar.Municipio', verbose_name=b'\xc2\xbfD\xc3\xb3nde lo vende?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comercializacion_cacao',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='certificacion',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='certificacion',
            name='paga_certificacion',
            field=models.ManyToManyField(to='monitoreo.Paga_Certifica', verbose_name=b'\xc2\xbfQui\xc3\xa9n paga la certificaci\xc3\xb3n?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='certificacion',
            name='quien_certifica',
            field=models.ManyToManyField(to='monitoreo.Quien_Certifica', verbose_name=b'\xc2\xbfQui\xc3\xa9n certifica?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='certificacion',
            name='tipo',
            field=models.ManyToManyField(to='monitoreo.Lista_Certificaciones', verbose_name=b'Tipo de certificaci\xc3\xb3n'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='caracterizacion_terreno',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='capacitaciones_tecnicas',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='capacitaciones_socioeconomicas',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area_cacao',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adicional',
            name='encuesta',
            field=models.ForeignKey(to='monitoreo.Encuesta'),
            preserve_default=True,
        ),
    ]
