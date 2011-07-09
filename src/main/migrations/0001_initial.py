# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('main_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('main', ['Category'])

        # Adding model 'Item'
        db.create_table('main_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Category'])),
            ('shop_cost', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cost', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Item'])

        # Adding model 'Resource'
        db.create_table('main_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resources', to=orm['main.Item'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='compose_set', to=orm['main.Item'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('main', ['Resource'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('main_category')

        # Deleting model 'Item'
        db.delete_table('main_item')

        # Deleting model 'Resource'
        db.delete_table('main_resource')


    models = {
        'main.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'main.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Category']"}),
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'shop_cost': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['main.Item']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'compose_set'", 'to': "orm['main.Item']"})
        }
    }

    complete_apps = ['main']
