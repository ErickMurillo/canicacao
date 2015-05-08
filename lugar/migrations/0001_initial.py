# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pais'
        db.create_table(u'lugar_pais', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'lugar', ['Pais'])

        # Adding model 'Departamento'
        db.create_table(u'lugar_departamento', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Pais'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True)),
            ('extension', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'lugar', ['Departamento'])

        # Adding model 'Municipio'
        db.create_table(u'lugar_municipio', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Departamento'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True)),
            ('extension', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('latitud', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5, blank=True)),
            ('longitud', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5, blank=True)),
        ))
        db.send_create_signal(u'lugar', ['Municipio'])

        # Adding model 'Comunidad'
        db.create_table(u'lugar_comunidad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lugar.Municipio'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'lugar', ['Comunidad'])


    def backwards(self, orm):
        # Deleting model 'Pais'
        db.delete_table(u'lugar_pais')

        # Deleting model 'Departamento'
        db.delete_table(u'lugar_departamento')

        # Deleting model 'Municipio'
        db.delete_table(u'lugar_municipio')

        # Deleting model 'Comunidad'
        db.delete_table(u'lugar_comunidad')


    models = {
        u'lugar.comunidad': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Comunidad'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lugar.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'lugar.departamento': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Departamento'},
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lugar.Pais']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'})
        },
        u'lugar.municipio': {
            'Meta': {'ordering': "['departamento__nombre', 'nombre']", 'object_name': 'Municipio'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lugar.Departamento']"}),
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'latitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'})
        },
        u'lugar.pais': {
            'Meta': {'object_name': 'Pais'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['lugar']