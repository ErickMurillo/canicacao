# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0004_auto_20150729_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizacion',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(default=1, upload_to=b'/logo_org'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='infraestructura',
            name='tipo',
            field=models.IntegerField(verbose_name=b'Tipo de Infraestructura', choices=[(1, b'Centro de Acopio central'), (2, b'Centro de acopio comunitarios'), (3, b'Hornos de secado'), (4, b'Planta de procesamiento'), (5, b'Bodegas'), (6, b'Cuartos fr\xc3\xados'), (7, b'Oficina'), (8, b'Medios de Transporte'), (9, b'\xc3\x81rea de fermentado'), (10, b'T\xc3\xbaneles de secado')]),
            preserve_default=True,
        ),
    ]
