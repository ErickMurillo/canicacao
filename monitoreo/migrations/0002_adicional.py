# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adicional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interes', models.IntegerField(verbose_name=b'Tiene interes en ampliar las \xc3\xa1reas de cacao', choices=[(1, b'Si'), (2, b'No')])),
                ('cuanto', models.FloatField()),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': 'Amplici\xf3n \xe1reas de cacao',
                'verbose_name_plural': 'Amplici\xf3n \xe1reas de cacao',
            },
            bases=(models.Model,),
        ),
    ]
