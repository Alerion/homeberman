# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Item', fields ['name']
        db.create_unique('main_item', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Item', fields ['name']
        db.delete_unique('main_item', ['name'])


    models = {
        'main.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'main.crafter': {
            'Meta': {'object_name': 'Crafter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'main.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Category']"}),
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'shop_cost': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['main.Item']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'compose_items'", 'to': "orm['main.Item']"})
        }
    }

    complete_apps = ['main']
