# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Item.craft_cost'
        db.add_column('main_item', 'craft_cost', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Item.craft_cost'
        db.delete_column('main_item', 'craft_cost')


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
            'craft_cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'crafter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Crafter']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Shop']", 'null': 'True', 'blank': 'True'}),
            'shop_cost': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['main.Item']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'compose_items'", 'to': "orm['main.Item']"})
        },
        'main.shop': {
            'Meta': {'object_name': 'Shop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['main']
