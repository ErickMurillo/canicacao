# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0006_auto_20150730_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tecnologias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Tecnolog\xeda de secado y almac. cacao',
                'verbose_name_plural': 'Tecnolog\xedas de secado y almac. cacao',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='mitigacion_riesgos',
            name='tecnologia_secado',
        ),
        migrations.AddField(
            model_name='mitigacion_riesgos',
            name='tecnologia_secado_1',
            field=models.ManyToManyField(to='monitoreo.Tecnologias', null=True, verbose_name=b'Mencione', blank=True),
            preserve_default=True,
        ),
    ]
