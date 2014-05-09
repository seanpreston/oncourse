# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'OAuthConsumer.user'
        db.delete_column('api_oauth_consumer', 'user_id')


    def backwards(self, orm):
        
        # Adding field 'OAuthConsumer.user'
        db.add_column('api_oauth_consumer', 'user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True), keep_default=False)


    models = {
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
