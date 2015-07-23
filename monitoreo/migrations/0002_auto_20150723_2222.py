# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import multiselectfield.db.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0002_auto_20150723_2221'),
        ('monitoreo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mitigacion_riesgos',
            name='d_tecnologia_secado',
            field=models.IntegerField(default=2, verbose_name=b'\xc2\xbfDispone de tecnolog\xc3\xada para el secado y almacenamiento de cosecha?', choices=[(1, b'Si'), (2, b'No')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plantacion',
            name='numero_plantas',
            field=models.IntegerField(default=2, verbose_name=b'N\xc3\xbamero de plantas en el \xc3\xa1rea'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recolector',
            name='organizacion',
            field=models.ForeignKey(default=2, to='organizacion.Organizacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uso_tierra',
            name='otros',
            field=models.FloatField(default=b'0', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='fecha',
            field=models.DateField(verbose_name=b'Fecha de la encuesta'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='organizacion',
            field=models.ForeignKey(verbose_name=b'Organizaci\xc3\xb3n que levanta datos', to='organizacion.Organizacion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='persona',
            field=models.ForeignKey(verbose_name=b'Nombre de la persona encuestada', to='monitoreo.Persona'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='recolector',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'organizacion', chained_field=b'organizacion', auto_choose=True, to='monitoreo.Recolector'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero',
            name='actividades',
            field=models.ManyToManyField(to='monitoreo.Actividades_Produccion', null=True, verbose_name=b'Actividades en las que participa', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero',
            name='decisiones',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, verbose_name=b'Decisiones sobre destino de la producci\xc3\xb3n', choices=[(1, b'Decide Usted sobre la siembra de cacao'), (2, b'Decide Usted sobre la cosecha de cacao'), (3, b'Decide Usted sobre la venta de cacao'), (4, b'Decide Usted sobre la Ingresos de cacao')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero',
            name='destino_ingresos',
            field=models.CharField(max_length=300, null=True, verbose_name=b'Destino de los ingresos percibidos', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero',
            name='ingresos',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfUsted recibe ingresos por las actividades que realiza?', choices=[(1, b'Si'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero_2',
            name='cacao',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Cacao', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero_2',
            name='cafe',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Caf\xc3\xa9', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero_2',
            name='ganaderia',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Ganader\xc3\xada', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero_2',
            name='granos_basicos',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Granos B\xc3\xa1sicos', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genero_2',
            name='madera',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Madera', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mitigacion_riesgos',
            name='tecnologia_secado',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Mencione', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problemas_cacao',
            name='arboles',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'\xc3\x81rboles poco productivos', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problemas_cacao',
            name='fertilidad',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Baja fertilidad del suelo', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problemas_cacao',
            name='mano_obra',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Poca disponibilidad de mano de obra', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problemas_cacao',
            name='plagas',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Plagas y enfermedades', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problemas_cacao',
            name='plantaciones',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Plantaciones muy viejas', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problemas_cacao',
            name='produccion',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Poca producci\xc3\xb3n', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='acopio_cacao',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Acopio de cacao en la comunidad/municipio', choices=[(1, b'Si'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='acopio_org',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Asociaci\xc3\xb3n con Org. que acopia cacao', choices=[(1, b'Si'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='fertilizacion',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=15, null=True, verbose_name=b'Pr\xc3\xa1cticas de fertilizaci\xc3\xb3n', choices=[(1, b'Aplicaci\xc3\xb3n de t\xc3\xa9 de esti\xc3\xa9rcol'), (2, b'Aplicaci\xc3\xb3n de gallinaza'), (3, b'Aplicaci\xc3\xb3n de Bocashi'), (4, b'Aplicaci\xc3\xb3n de foliares naturales'), (5, b'Uso de triple cal'), (6, b'Aplicaci\xc3\xb3n de lombrihumus'), (7, b'Aplicaci\xc3\xb3n de urea'), (8, b'Aplicaci\xc3\xb3n de fertilizante completo')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='pract_manejo_fis',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=11, null=True, verbose_name=b'Pr\xc3\xa1cticas de manejo fitosanitario', choices=[(1, b'Control de malas hierbas con machete'), (2, b'Aplica herbicidas para controlar las malas hierbas'), (3, b'Manejo de plagas con productos naturales'), (4, b'Manejo de enfermedades con productos naturales'), (5, b'Manejo de enfermedades con fungicidas'), (6, b'Recolecci\xc3\xb3n e eliminaci\xc3\xb3n de frutos enfermos')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='pract_manejo_post_c',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=15, null=True, verbose_name=b'Pr\xc3\xa1cticas de manejo postcosecha y beneficiado', choices=[(1, b'Selecci\xc3\xb3n y clasificaci\xc3\xb3n de mazorcas por variedad'), (2, b'Selecci\xc3\xb3n de cacao en baba a fermentar'), (3, b'Fermentaci\xc3\xb3n en sacos'), (4, b'Fermentaci\xc3\xb3n en cajones'), (5, b'Fermentaci\xc3\xb3n en cajillas'), (6, b'Lo vende en baba a un centro de acopio'), (7, b'Solo la saca de la mazorca y lo seca'), (8, b'Lo saca de la mazorca, lo lava y luego lo seca')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='pract_manejo_prod',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, verbose_name=b'Pr\xc3\xa1cticas de manejo productivo', choices=[(1, b'Poda de formaci\xc3\xb3n'), (2, b'Poda de mantenimiento'), (3, b'Poda de rehabilitaci\xc3\xb3n o renovaci\xc3\xb3n'), (4, b'Regulaci\xc3\xb3n en sombra')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='pract_mejora_plat',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, verbose_name=b'Pr\xc3\xa1cticas de mejoramiento de la plantaci\xc3\xb3n', choices=[(1, b'Selecci\xc3\xb3n de \xc3\xa1rboles superiores'), (2, b'Injertaci\xc3\xb3n en \xc3\xa1rboles adultos'), (3, b'Renovaci\xc3\xb3n de \xc3\xa1rea con plantas injertadas'), (4, b'Enriquecimiento de \xc3\xa1reas con plantas injertadas')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tecnicas_aplicadas',
            name='viveros',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=15, null=True, choices=[(1, b'Preparaci\xc3\xb3n del sitio'), (2, b'Preparaci\xc3\xb3n del sustrato'), (3, b'Llenado de bolsa'), (4, b'Selecci\xc3\xb3n de semilla'), (5, b'Siembra de semilla'), (6, b'Uso de riego'), (7, b'Control de malas hierba'), (8, b'Fertilizaci\xc3\xb3n org\xc3\xa1nica')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='persona',
            unique_together=set([('cedula',)]),
        ),
    ]
