# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'AccessToken', fields ['token']
        db.create_index('api_accesstoken', ['token'])

        # Adding unique constraint on 'AccessToken', fields ['token']
        db.create_unique('api_accesstoken', ['token'])

        # Adding index on 'OAuthConsumer', fields ['active']
        db.create_index('api_oauth_consumer', ['active'])

        # Adding index on 'OAuthConsumer', fields ['secret']
        db.create_index('api_oauth_consumer', ['secret'])

        # Adding unique constraint on 'OAuthConsumer', fields ['secret']
        db.create_unique('api_oauth_consumer', ['secret'])

        # Adding index on 'OAuthConsumer', fields ['key']
        db.create_index('api_oauth_consumer', ['key'])

        # Adding unique constraint on 'OAuthConsumer', fields ['key']
        db.create_unique('api_oauth_consumer', ['key'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'OAuthConsumer', fields ['key']
        db.delete_unique('api_oauth_consumer', ['key'])

        # Removing index on 'OAuthConsumer', fields ['key']
        db.delete_index('api_oauth_consumer', ['key'])

        # Removing unique constraint on 'OAuthConsumer', fields ['secret']
        db.delete_unique('api_oauth_consumer', ['secret'])

        # Removing index on 'OAuthConsumer', fields ['secret']
        db.delete_index('api_oauth_consumer', ['secret'])

        # Removing index on 'OAuthConsumer', fields ['active']
        db.delete_index('api_oauth_consumer', ['active'])

        # Removing unique constraint on 'AccessToken', fields ['token']
        db.delete_unique('api_accesstoken', ['token'])

        # Removing index on 'AccessToken', fields ['token']
        db.delete_index('api_accesstoken', ['token'])


    models = {
        'api.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'consumer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.OAuthConsumer']"}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'962a3c16041b9bba297c311e6ae0b050'", 'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'access_tokens'", 'to': "orm['auth.User']"})
        },
        'api.lastvisited': {
            'Meta': {'object_name': 'LastVisited', 'db_table': "'api_last_visited'"},
            'activity': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'api.oauthconsumer': {
            'Meta': {'object_name': 'OAuthConsumer', 'db_table': "'api_oauth_consumer'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'1dc991f270fb62aef0869f419753df3f'", 'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'579560699ec7f6cbd21579fbc92ce298'", 'unique': 'True', 'max_length': '255', 'db_index': 'True'})
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 12, 17, 59, 20, 208666)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 12, 17, 59, 20, 208591)'}),
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
        }
    }

    complete_apps = ['api']
