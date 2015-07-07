# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import smart_selects.db_fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('lugar', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades_Produccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Actividad de Producci\xf3n',
                'verbose_name_plural': 'Actividades de Producci\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Adicional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interes', models.IntegerField(verbose_name=b'Tiene interes en ampliar las \xc3\xa1reas de cacao', choices=[(1, b'Si'), (2, b'No')])),
                ('cuanto', models.FloatField()),
            ],
            options={
                'verbose_name': 'Amplici\xf3n \xe1reas de cacao',
                'verbose_name_plural': 'Amplici\xf3n \xe1reas de cacao',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Area_Cacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.FloatField(verbose_name=b'\xc3\x81rea total de cacao establecida en finca(Mz)')),
            ],
            options={
                'verbose_name': '9 \xc1rea de cacao en finca',
                'verbose_name_plural': '9 \xc1rea de cacao en fincas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Beneficios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beneficio', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Beneficio',
                'verbose_name_plural': 'Beneficios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Capacitaciones_Socioeconomicas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capacitaciones_socio', models.IntegerField(verbose_name=b'Capacitaciones', choices=[(1, b'Formaci\xc3\xb3n y fortalecimiento organizacional'), (2, b'Contabilidad b\xc3\xa1sica y administraci\xc3\xb3n'), (3, b'Equidad de g\xc3\xa9nero'), (4, b'Manejo de cr\xc3\xa9ditos'), (5, b'Administraci\xc3\xb3n de peque\xc3\xb1os negocios'), (6, b'Gesti\xc3\xb3n empresarial'), (7, b'Cadena de valor de cacao'), (8, b'Transformaci\xc3\xb3n de cacao')])),
                ('opciones_socio', multiselectfield.db.fields.MultiSelectField(max_length=7, verbose_name=b'Opciones', choices=[(1, b'Jefe familia var\xc3\xb3n'), (2, b'Jefa familia mujer'), (3, b'Hijos'), (4, b'Hijas')])),
            ],
            options={
                'verbose_name': '13.2 Capacitaciones socioecon\xf3mico/org',
                'verbose_name_plural': '13.2 Capacitaciones socioecon\xf3mico/org',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Capacitaciones_Tecnicas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capacitaciones', models.IntegerField(choices=[(1, b'Regular en sombra'), (2, b'Poda'), (3, b'Manejo de plagas y enfermedades'), (4, b'Elaboraci\xc3\xb3n de abonos org\xc3\xa1nicos'), (5, b'Elaboraci\xc3\xb3n de productos para control de plagas'), (6, b'Establecimiento de vivero'), (7, b'Injertaci\xc3\xb3n de cacao'), (8, b'Selecci\xc3\xb3n de \xc3\xa1rboles \xc3\xa9lites para producci\xc3\xb3n de semillas'), (9, b'Manejo de post-cosecha (selecci\xc3\xb3n, cosecha, fermentado, secado)'), (10, b'Manejo de calidad de cacao'), (11, b'Certificaci\xc3\xb3n org\xc3\xa1nica')])),
                ('opciones', multiselectfield.db.fields.MultiSelectField(max_length=7, choices=[(1, b'Jefe familia var\xc3\xb3n'), (2, b'Jefa familia mujer'), (3, b'Hijos'), (4, b'Hijas')])),
            ],
            options={
                'verbose_name': '13.1 Capacitaci\xf3n familia',
                'verbose_name_plural': '13.1 Capacitaci\xf3n familia',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Caracterizacion_Terreno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('textura_suelo', models.IntegerField(verbose_name=b'\xc2\xbfCu\xc3\xa1l es el tipo de textura del suelo?', choices=[(1, b'Arcilloso'), (2, b'Limoso'), (3, b'Arenoso'), (4, b'Franco'), (5, b'Franco arenoso')])),
                ('pendiente_terreno', models.IntegerField(verbose_name=b'\xc2\xbfCu\xc3\xa1l es la pendiente del terreno?', choices=[(1, b'Plana'), (2, b'Inclinada'), (3, b'Muy inclinada')])),
                ('contenido_hojarasca', models.IntegerField(verbose_name=b'\xc2\xbfC\xc3\xb3mo en el contenido de hojarasca?', choices=[(1, b'Alta'), (2, b'Medio'), (3, b'Baja')])),
                ('porfundidad_suelo', models.IntegerField(verbose_name=b'\xc2\xbfCu\xc3\xa1l es la profundidad de suelo?', choices=[(1, b'Poco profundo'), (2, b'Medio profundo'), (3, b'Muy profundo')])),
                ('drenaje_suelo', models.IntegerField(verbose_name=b'\xc2\xbfC\xc3\xb3mo en el drenaje del suelo?', choices=[(1, b'Bueno'), (2, b'Regular'), (3, b'Malo')])),
            ],
            options={
                'verbose_name': '5 Caracterizaci\xf3n de terreno',
                'verbose_name_plural': '5 Caracterizaci\xf3n de terreno',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Certificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mant_area_cacao', models.FloatField(verbose_name=b'Mantenimiento de \xc3\xa1rea de cacao (C$)')),
                ('mant_area_finca', models.FloatField(verbose_name=b'Mantenimiento de la finca (C$)')),
                ('costo_ccertificacion', models.FloatField(verbose_name=b'Costo de estar certificado')),
            ],
            options={
                'verbose_name': '10-1 Tipo de certificaci\xf3n que posee',
                'verbose_name_plural': '10-1 Tipo de certificaci\xf3n que posee',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comercializacion_Cacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('producto', models.IntegerField(choices=[(1, b'Mazorca de cacao (unidad)'), (2, b'Semilla para siembra (unidad)'), (3, b'Cacao en baba (qq)'), (4, b'Cacao rojo sin fermentar (qq)'), (5, b'Cacao fermentado (lb)'), (6, b'Chocolate artesanal (lb)'), (7, b'Cacao en polvo (lb)'), (8, b'Cacao procesado/ pinolillo (lb)'), (9, b'Cajeta de cacao (lb)'), (10, b'Pasta de cacao (lb)'), (11, b'Vino de cacao (lt)')])),
                ('auto_consumo', models.FloatField(verbose_name=b'Auto-consumo')),
                ('venta', models.FloatField()),
                ('precio_venta', models.FloatField(verbose_name=b'Precio venta por unidad')),
                ('quien_vende', multiselectfield.db.fields.MultiSelectField(max_length=7, verbose_name=b'\xc2\xbfA qui\xc3\xa9n le vende?', choices=[(1, b'Comunidad'), (2, b'Intermediario'), (3, b'Mercado'), (4, b'Cooperativa')])),
            ],
            options={
                'verbose_name': '12 Comercializaci\xf3n de cacao',
                'verbose_name_plural': '12 Comercializaci\xf3n de cacao',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Distancia_Comercio_Cacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distancia', models.FloatField()),
            ],
            options={
                'verbose_name': '12.1 Distancia recorrida (Km)',
                'verbose_name_plural': '12.1 Distancia recorrida (Km)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Educacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rango', models.IntegerField(verbose_name=b'Selecci\xc3\xb3n', choices=[(1, b'Hombres mayores 31 a\xc3\xb1os'), (2, b'Mujeres mayores 31 a\xc3\xb1os'), (3, b'Hombre joven 19 a 30 a\xc3\xb1os'), (4, b'Mujer joven 19 a 30 a\xc3\xb1os'), (5, b'Hombre adoles. 13 a 18 a\xc3\xb1os'), (6, b'Mujer adoles. 13 a 18 a\xc3\xb1os'), (7, b'Ni\xc3\xb1os 0 a 12 a\xc3\xb1os'), (8, b'Ni\xc3\xb1as 0 a 12 a\xc3\xb1os'), (9, b'Ancianos (> 64 a\xc3\xb1os)')])),
                ('numero_total', models.IntegerField()),
                ('no_lee_ni_escribe', models.IntegerField()),
                ('primaria_incompleta', models.IntegerField()),
                ('primaria_completa', models.IntegerField()),
                ('secundaria_incompleta', models.IntegerField()),
                ('bachiller', models.IntegerField()),
                ('universitario_tecnico', models.IntegerField()),
                ('viven_fuera', models.IntegerField(verbose_name=b'N\xc3\xbamero de personas que viven fuera de la finca')),
            ],
            options={
                'verbose_name': '1-2 Nivel de educaci\xf3n de la Familia',
                'verbose_name_plural': '1-2 Nivel de educaci\xf3n de la Familia',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('anno', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('miembros', models.IntegerField(verbose_name=b'N\xc3\xbamero de miembros')),
            ],
            options={
                'verbose_name': '1-1 Miembros de la Familia',
                'verbose_name_plural': '1-1 Miembros de la Familia',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fenomenos_Naturales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequia', models.IntegerField(verbose_name=b'Sequ\xc3\xada', choices=[(1, b'Fuerte'), (2, b'Poco fuerte'), (3, b'Leve'), (4, b'No hubo')])),
                ('innundacion', models.IntegerField(verbose_name=b'Inundaci\xc3\xb3n', choices=[(1, b'Fuerte'), (2, b'Poco fuerte'), (3, b'Leve'), (4, b'No hubo')])),
                ('lluvia', models.IntegerField(choices=[(1, b'Fuerte'), (2, b'Poco fuerte'), (3, b'Leve'), (4, b'No hubo')])),
                ('viento', models.IntegerField(choices=[(1, b'Fuerte'), (2, b'Poco fuerte'), (3, b'Leve'), (4, b'No hubo')])),
                ('deslizamiento', models.IntegerField(choices=[(1, b'Fuerte'), (2, b'Poco fuerte'), (3, b'Leve'), (4, b'No hubo')])),
            ],
            options={
                'verbose_name': '6 Fen\xf3menos naturales',
                'verbose_name_plural': '6 Fen\xf3menos naturales',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ingresos', models.IntegerField(verbose_name=b'\xc2\xbfUsted recibe ingresos por las actividades que realiza?', choices=[(1, b'Si'), (2, b'No')])),
                ('ingreso_mesual', models.FloatField(null=True, verbose_name=b'Ingreso mensual aproximado percibido', blank=True)),
                ('destino_ingresos', models.CharField(max_length=300, verbose_name=b'Destino de los ingresos percibidos')),
                ('decisiones', multiselectfield.db.fields.MultiSelectField(max_length=7, verbose_name=b'Decisiones sobre destino de la producci\xc3\xb3n', choices=[(1, b'Decide Usted sobre la siembra de cacao'), (2, b'Decide Usted sobre la cosecha de cacao'), (3, b'Decide Usted sobre la venta de cacao'), (4, b'Decide Usted sobre la Ingresos de cacao')])),
            ],
            options={
                'verbose_name': '14 G\xe9nero',
                'verbose_name_plural': '14 G\xe9nero',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genero_2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ganaderia', models.IntegerField(verbose_name=b'Ganader\xc3\xada', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('granos_basicos', models.IntegerField(verbose_name=b'Granos B\xc3\xa1sicos', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('cacao', models.IntegerField(verbose_name=b'Cacao', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('cafe', models.IntegerField(verbose_name=b'Caf\xc3\xa9', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('madera', models.IntegerField(verbose_name=b'Madera', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
            ],
            options={
                'verbose_name': 'Sobre otros Ingresos',
                'verbose_name_plural': 'Sobre otros Ingresos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invierte_cacao', models.IntegerField(verbose_name=b'Invierte en cacao', choices=[(1, b'Si'), (2, b'No')])),
                ('interes_invertrir', models.IntegerField(verbose_name=b'Inter\xc3\xa9s de invertir', choices=[(1, b'Si'), (2, b'No')])),
                ('falta_credito', models.IntegerField(verbose_name=b'Falta de cr\xc3\xa9dito', choices=[(1, b'Si'), (2, b'No')])),
                ('altos_intereses', models.IntegerField(choices=[(1, b'Si'), (2, b'No')])),
                ('robo_producto', models.IntegerField(verbose_name=b'Robo de producto', choices=[(1, b'Si'), (2, b'No')])),
            ],
            options={
                'verbose_name': '6 Inversi\xf3n',
                'verbose_name_plural': '6 Inversi\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lista_Certificaciones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Certificaci\xf3n',
                'verbose_name_plural': 'Certificaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mitigacion_Riesgos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monitoreo_plagas', models.IntegerField(verbose_name=b'\xc2\xbfRealiza monitoreo de plagas y enfermedades?', choices=[(1, b'Si'), (2, b'No')])),
                ('manejo_cultivo', models.IntegerField(verbose_name=b'\xc2\xbfCuenta con un manejo adecuado para el cultivo?', choices=[(1, b'Si'), (2, b'No')])),
                ('manejo_recursos', models.IntegerField(verbose_name=b'\xc2\xbfDisponen suficiente recursos para manejo de finca?', choices=[(1, b'Si'), (2, b'No')])),
                ('almacenamiento_agua', models.IntegerField(verbose_name=b'\xc2\xbfCuenta con obras para almacenamiento de agua?', choices=[(1, b'Si'), (2, b'No')])),
                ('distribucion_cacao', models.IntegerField(verbose_name=b'\xc2\xbfParticipan en cadena de distribuci\xc3\xb3n de producto cacao?', choices=[(1, b'Si'), (2, b'No')])),
                ('venta_cacao', models.IntegerField(verbose_name=b'\xc2\xbfCuenta con un contrato para la venta de cacao?', choices=[(1, b'Si'), (2, b'No')])),
                ('tecnologia_secado', models.CharField(max_length=200, null=True, verbose_name=b'\xc2\xbfDispone de tecnolog\xc3\xada para el secado y almacenamiento de cosecha? Mencione', blank=True)),
            ],
            options={
                'verbose_name': '7 Mitigaci\xf3n de Riesgos',
                'verbose_name_plural': '7 Mitigaci\xf3n de Riesgos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organizacion_Asociada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beneficios', models.ManyToManyField(to='monitoreo.Beneficios', verbose_name=b'Beneficios de estar asociado')),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '8 Org. productiva-comercial asociado',
                'verbose_name_plural': '8 Org. productiva-comercial asociado',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paga_Certifica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Qui\xe9n paga la certifica',
                'verbose_name_plural': 'Quienes pagan la certificaci\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200, verbose_name=b'Nombre de jefa/e de familia')),
                ('cedula', models.CharField(max_length=20, null=True, verbose_name=b'C\xc3\xa9ula de entrevistado/a', blank=True)),
                ('fecha_nacimiento', models.DateField(verbose_name=b'Fecha de nacimiento')),
                ('sexo', models.IntegerField(choices=[(1, b'Hombre'), (2, b'Mujer')])),
                ('profesion', models.IntegerField(choices=[(1, b'Agricultor(a)'), (2, b'Profesor(a)')])),
                ('latitud', models.FloatField(null=True, blank=True)),
                ('longitud', models.FloatField(null=True, blank=True)),
                ('comunidad', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'municipio', chained_field=b'municipio', auto_choose=True, to='lugar.Comunidad')),
                ('departamento', models.ForeignKey(to='lugar.Departamento')),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'departamento', chained_field=b'departamento', auto_choose=True, to='lugar.Municipio')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plantacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edad', models.IntegerField(choices=[(1, b'Menor de un a\xc3\xb1o'), (2, b'De 1 a 3 a\xc3\xb1os'), (3, b'De 4 a 10 a\xc3\xb1os'), (4, b'De 10 a 20 a\xc3\xb1os'), (5, b'Mayores de 20 a\xc3\xb1os')])),
                ('area', models.FloatField(verbose_name=b'\xc3\x81rea en Mz')),
                ('edad_real', models.FloatField(verbose_name=b'Edad real de la Plantaci\xc3\xb3n (a\xc3\xb1os)')),
                ('numero_p_semilla', models.IntegerField(verbose_name=b'N\xc3\xbamero de plantas establecidas por semilla')),
                ('numero_p_injerto', models.IntegerField(verbose_name=b'N\xc3\xbamero de plantas establecidas por injerto')),
                ('numero_p_improductivas', models.IntegerField(verbose_name=b'N\xc3\xbamero de plantas improductivas en el \xc3\xa1rea')),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '9-1 Edad de la plantaci\xf3n',
                'verbose_name_plural': '9-1 Edad de la plantaci\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Problemas_Cacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fertilidad', models.IntegerField(verbose_name=b'Baja fertilidad del suelo', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('arboles', models.IntegerField(verbose_name=b'\xc3\x81rboles poco productivos', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('plantaciones', models.IntegerField(verbose_name=b'Plantaciones muy viejas', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('plagas', models.IntegerField(verbose_name=b'Plagas y enfermedades', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('produccion', models.IntegerField(verbose_name=b'Poca producci\xc3\xb3n', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('mano_obra', models.IntegerField(verbose_name=b'Poca disponibilidad de mano de obra', choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '13.3 Problemas \xe1rea de cacao',
                'verbose_name_plural': '13.3 Problemas \xe1rea de cacao',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produccion_Cacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('produccion_c_baba', models.FloatField(verbose_name=b'Producci\xc3\xb3n cacao en baba (qq baba/seco)')),
                ('produccion_c_seco', models.FloatField(verbose_name=b'Producci\xc3\xb3n cacao seco sin fermentar (qq seco)')),
                ('produccion_c_fermentado', models.FloatField(verbose_name=b'Producci\xc3\xb3n cacao fermentado convencional (qq seco)')),
                ('produccion_c_organico', models.FloatField(verbose_name=b'Producci\xc3\xb3n cacao organico (qq seco)')),
                ('meses_produccion', multiselectfield.db.fields.MultiSelectField(max_length=26, verbose_name=b'Meses de mayor producci\xc3\xb3n de cacao', choices=[(1, b'Enero'), (2, b'Febrero'), (3, b'Marzo'), (4, b'Abril'), (5, b'Mayo'), (6, b'Junio'), (7, b'Julio'), (8, b'Agosto'), (9, b'Septiembre'), (10, b'Octubre'), (11, b'Noviembre'), (12, b'Diciembre')])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '9-2 Producci\xf3n de cacao \xfaltimo a\xf1o',
                'verbose_name_plural': '9-2 Producci\xf3n de cacao \xfaltimo a\xf1o',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quien_Certifica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Qui\xe9n certifica',
                'verbose_name_plural': 'Quienes certifican',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Razones_Agricolas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plantas_improductivas', models.IntegerField(choices=[(1, b'Alto (40%)'), (2, b'Medio (30%)'), (3, b'Baja (10%)')])),
                ('plagas_enfermedades', models.IntegerField(verbose_name=b'Plagas y enfermedades', choices=[(1, b'Si'), (2, b'No')])),
                ('quemas', models.IntegerField(choices=[(1, b'Si'), (2, b'No')])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '6 Razones agr\xedcolas',
                'verbose_name_plural': '6 Razones agr\xedcolas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Razones_Mercado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bajo_precio', models.IntegerField(choices=[(1, b'Si'), (2, b'No')])),
                ('falta_venta', models.IntegerField(verbose_name=b'Falta de venta', choices=[(1, b'Si'), (2, b'No')])),
                ('estafa_contrato', models.IntegerField(verbose_name=b'Estafa de contrato', choices=[(1, b'Si'), (2, b'No')])),
                ('calidad_producto', models.IntegerField(verbose_name=b'Mala calidad de producto', choices=[(1, b'Si'), (2, b'No')])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '6 Razones de mercado',
                'verbose_name_plural': '6 Razones de mercado',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recolector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Recolector',
                'verbose_name_plural': 'Recolectores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reforestacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enriquecimiento_bosques', models.IntegerField(verbose_name=b'Enriquecimiento de los bosques', choices=[(1, b'Si'), (2, b'No')])),
                ('proteccion_agua', models.IntegerField(verbose_name=b'Protecci\xc3\xb3n de fuentes de agua', choices=[(1, b'Si'), (2, b'No')])),
                ('cercas_vivas', models.IntegerField(verbose_name=b'Establecimiento de cercas viva', choices=[(1, b'Si'), (2, b'No')])),
                ('viveros', models.IntegerField(verbose_name=b'Establecimiento de viveros', choices=[(1, b'Si'), (2, b'No')])),
                ('siembre_cacao', models.IntegerField(verbose_name=b'Siembra de \xc3\xa1rboles en cacao', choices=[(1, b'Si'), (2, b'No')])),
                ('forestales', models.IntegerField(verbose_name=b'Plantaciones forestales', choices=[(1, b'Si'), (2, b'No')])),
                ('potrero', models.IntegerField(verbose_name=b'Siembra de \xc3\xa1rboles en potrero', choices=[(1, b'Si'), (2, b'No')])),
                ('frutales', models.IntegerField(verbose_name=b'Parcelas frutales', choices=[(1, b'Si'), (2, b'No')])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '4 Reforestaci\xf3n',
                'verbose_name_plural': '4 Reforestaci\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Situacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Situaci\xf3n',
                'verbose_name_plural': 'Situaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tecnicas_Aplicadas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('viveros', multiselectfield.db.fields.MultiSelectField(max_length=15, choices=[(1, b'Preparaci\xc3\xb3n del sitio'), (2, b'Preparaci\xc3\xb3n del sustrato'), (3, b'Llenado de bolsa'), (4, b'Selecci\xc3\xb3n de semilla'), (5, b'Siembra de semilla'), (6, b'Uso de riego'), (7, b'Control de malas hierba'), (8, b'Fertilizaci\xc3\xb3n org\xc3\xa1nica')])),
                ('fertilizacion', multiselectfield.db.fields.MultiSelectField(max_length=15, verbose_name=b'Pr\xc3\xa1cticas de fertilizaci\xc3\xb3n', choices=[(1, b'Aplicaci\xc3\xb3n de t\xc3\xa9 de esti\xc3\xa9rcol'), (2, b'Aplicaci\xc3\xb3n de gallinaza'), (3, b'Aplicaci\xc3\xb3n de Bocashi'), (4, b'Aplicaci\xc3\xb3n de foliares naturales'), (5, b'Uso de triple cal'), (6, b'Aplicaci\xc3\xb3n de lombrihumus'), (7, b'Aplicaci\xc3\xb3n de urea'), (8, b'Aplicaci\xc3\xb3n de fertilizante completo')])),
                ('pract_manejo_fis', multiselectfield.db.fields.MultiSelectField(max_length=11, verbose_name=b'Pr\xc3\xa1cticas de manejo fitosanitario', choices=[(1, b'Control de malas hierbas con machete'), (2, b'Aplica herbicidas para controlar las malas hierbas'), (3, b'Manejo de plagas con productos naturales'), (4, b'Manejo de enfermedades con productos naturales'), (5, b'Manejo de enfermedades con fungicidas'), (6, b'Recolecci\xc3\xb3n e eliminaci\xc3\xb3n de frutos enfermos')])),
                ('pract_manejo_prod', multiselectfield.db.fields.MultiSelectField(max_length=7, verbose_name=b'Pr\xc3\xa1cticas de manejo productivo', choices=[(1, b'Poda de formaci\xc3\xb3n'), (2, b'Poda de mantenimiento'), (3, b'Poda de rehabilitaci\xc3\xb3n o renovaci\xc3\xb3n'), (4, b'Regulaci\xc3\xb3n en sombra')])),
                ('pract_mejora_plat', multiselectfield.db.fields.MultiSelectField(max_length=7, verbose_name=b'Pr\xc3\xa1cticas de mejoramiento de la plantaci\xc3\xb3n', choices=[(1, b'Selecci\xc3\xb3n de \xc3\xa1rboles superiores'), (2, b'Injertaci\xc3\xb3n en \xc3\xa1rboles adultos'), (3, b'Renovaci\xc3\xb3n de \xc3\xa1rea con plantas injertadas'), (4, b'Enriquecimiento de \xc3\xa1reas con plantas injertadas')])),
                ('pract_manejo_post_c', multiselectfield.db.fields.MultiSelectField(max_length=15, verbose_name=b'Pr\xc3\xa1cticas de manejo postcosecha y beneficiado', choices=[(1, b'Selecci\xc3\xb3n y clasificaci\xc3\xb3n de mazorcas por variedad'), (2, b'Selecci\xc3\xb3n de cacao en baba a fermentar'), (3, b'Fermentaci\xc3\xb3n en sacos'), (4, b'Fermentaci\xc3\xb3n en cajones'), (5, b'Fermentaci\xc3\xb3n en cajillas'), (6, b'Lo vende en baba a un centro de acopio'), (7, b'Solo la saca de la mazorca y lo seca'), (8, b'Lo saca de la mazorca, lo lava y luego lo seca')])),
                ('acopio_cacao', models.IntegerField(verbose_name=b'Acopio de cacao en la comunidad/municipio', choices=[(1, b'Si'), (2, b'No')])),
                ('acopio_org', models.IntegerField(verbose_name=b'Asociaci\xc3\xb3n con Org. que acopia cacao', choices=[(1, b'Si'), (2, b'No')])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '11 T\xe9cn. aplicadas \xe1rea de cacao',
                'verbose_name_plural': '11 T\xe9cn. aplicadas \xe1rea de cacao',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tenencia_Propiedad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si', models.IntegerField(blank=True, null=True, verbose_name=b'En el caso Si, a nombre de quien esta la propiedad', choices=[(1, b'A nombre del Hombre'), (2, b'A nombre de la Mujer'), (3, b'A nombre de Hijas/hijos'), (4, b'A nombre del Hombre y Mujer'), (5, b'Colectivo')])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
                ('no', models.ForeignKey(verbose_name=b'En el caso que diga NO, especifique la situaci\xc3\xb3n', blank=True, to='monitoreo.Situacion', null=True)),
            ],
            options={
                'verbose_name': '2 Tenencia de Propiedad',
                'verbose_name_plural': '2 Tenencia de Propiedad',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipos_Servicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('servicio', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Tipo de Servicio',
                'verbose_name_plural': 'Tipos de Servicios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uso_Tierra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area_total', models.FloatField(verbose_name=b'\xc3\x81rea total en manzanas de la propiedad', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)])),
                ('bosque', models.FloatField(verbose_name=b'Bosques', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('tacotal', models.FloatField(verbose_name=b'Tacotal o \xc3\xa1rea de descanso', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('cultivo_anual', models.FloatField(verbose_name=b'Cultivo anual ( que produce en el a\xc3\xb1o)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('plantacion_forestal', models.FloatField(verbose_name=b'Plantaci\xc3\xb3n forestal ( madera y le\xc3\xb1a)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('area_pasto_abierto', models.FloatField(verbose_name=b'\xc3\x81rea de pastos abierto', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('area_pasto_arboles', models.FloatField(verbose_name=b'\xc3\x81rea de pastos con \xc3\xa1rboles', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('cultivo_perenne', models.FloatField(verbose_name=b'Cultivo perenne (frutales)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('cultivo_semi_perenne', models.FloatField(verbose_name=b'Cultivo semi-perenne (mus\xc3\xa1cea, pi\xc3\xb1a)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('cacao', models.FloatField(verbose_name=b'Solo destinado para cacao', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('huerto_mixto_cacao', models.FloatField(verbose_name=b'Huerto mixto con cacao', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('encuesta', models.ForeignKey(to='monitoreo.Encuesta')),
            ],
            options={
                'verbose_name': '3 Uso de Tierra',
                'verbose_name_plural': '3 Uso de Tierra',
            },
            bases=(models.Model,),
        ),
    ]
