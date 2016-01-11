# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0003_auto_20150725_0630'),
        ('monitoreo', '0002_auto_20150723_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='organizacion',
            field=models.ForeignKey(default=1, verbose_name=b'A que Organizaci\xc3\xb3n pertenece', to='organizacion.Organizacion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comercializacion_cacao',
            name='auto_consumo',
            field=models.FloatField(null=True, verbose_name=b'Auto-consumo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializacion_cacao',
            name='donde_vende',
            field=models.ManyToManyField(to='lugar.Municipio', null=True, verbose_name=b'\xc2\xbfD\xc3\xb3nde lo vende?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializacion_cacao',
            name='precio_venta',
            field=models.FloatField(null=True, verbose_name=b'Precio venta por unidad', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializacion_cacao',
            name='quien_vende',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, verbose_name=b'\xc2\xbfA qui\xc3\xa9n le vende?', choices=[(1, b'Comunidad'), (2, b'Intermediario'), (3, b'Mercado'), (4, b'Cooperativa')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializacion_cacao',
            name='venta',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='persona',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'organizacion', chained_field=b'organizacion', auto_choose=True, to='monitoreo.Persona'),
            preserve_default=True,
        ),
    ]
