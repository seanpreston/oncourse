# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'LastVisited'
        db.create_table('api_last_visited', (
            ('user_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.DateTimeField')()),
            ))
        db.send_create_signal('api', ['LastVisited'])

    def backwards(self, orm):

        # Removing model 'LastVisited'
        db.delete_table('api_last_visited')

    models = {
        'api.lastvisited': {
            'Meta': {'object_name': 'LastVisited', 'db_table': "'api_last_visited'"},
            'activity': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'api.oauthconsumer': {
            'Meta': {'object_name': 'OAuthConsumer', 'db_table': "'api_oauth_consumer'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['api']

    models = {
        'api.lastvisited': {
            'Meta': {'object_name': 'LastVisited', 'db_table': "'api_last_visited'"},
            'activity': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'api.oauthconsumer': {
            'Meta': {'object_name': 'OAuthConsumer', 'db_table': "'api_oauth_consumer'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
