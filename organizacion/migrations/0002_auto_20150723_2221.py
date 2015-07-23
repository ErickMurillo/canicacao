# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizacion',
            name='direccion',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizacion',
            name='fundacion',
            field=models.DateField(null=True, verbose_name=b'A\xc3\xb1o fundaci\xc3\xb3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizacion',
            name='gerente',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Director/Gerente', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizacion',
            name='status',
            field=models.ForeignKey(verbose_name=b'Status Legal', blank=True, to='organizacion.Status', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='organizacion',
            unique_together=set([('nombre',)]),
        ),
    ]
