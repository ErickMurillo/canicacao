# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0005_auto_20151109_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizacion',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b'logo_org/', blank=True),
            preserve_default=True,
        ),
    ]
