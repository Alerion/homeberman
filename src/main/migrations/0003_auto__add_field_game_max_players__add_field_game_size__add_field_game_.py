# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Game.max_players'
        db.add_column('main_game', 'max_players', self.gf('django.db.models.fields.PositiveIntegerField')(default=10), keep_default=False)

        # Adding field 'Game.size'
        db.add_column('main_game', 'size', self.gf('django.db.models.fields.CharField')(default='small', max_length=10), keep_default=False)

        # Adding field 'Game.winner'
        db.add_column('main_game', 'winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winned_games', null=True, to=orm['main.Player']), keep_default=False)

        # Changing field 'Cell.type'
        db.alter_column('main_cell', 'type', self.gf('django.db.models.fields.IntegerField')())

        # Adding field 'Player.is_dead'
        db.add_column('main_player', 'is_dead', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Player.last_move_time'
        db.add_column('main_player', 'last_move_time', self.gf('django.db.models.fields.BigIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Game.max_players'
        db.delete_column('main_game', 'max_players')

        # Deleting field 'Game.size'
        db.delete_column('main_game', 'size')

        # Deleting field 'Game.winner'
        db.delete_column('main_game', 'winner_id')

        # Changing field 'Cell.type'
        db.alter_column('main_cell', 'type', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Deleting field 'Player.is_dead'
        db.delete_column('main_player', 'is_dead')

        # Deleting field 'Player.last_move_time'
        db.delete_column('main_player', 'last_move_time')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.cell': {
            'Meta': {'unique_together': "(('game', 'x', 'y'),)", 'object_name': 'Cell'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cells'", 'to': "orm['main.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.game': {
            'Meta': {'object_name': 'Game'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_players': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'small'", 'max_length': '10'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winned_games'", 'null': 'True', 'to': "orm['main.Player']"})
        },
        'main.player': {
            'Meta': {'object_name': 'Player'},
            'cell': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Cell']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_move_time': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"})
        }
    }

    complete_apps = ['main']
