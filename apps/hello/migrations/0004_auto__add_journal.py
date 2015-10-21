# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Journal'
        db.create_table(u'hello_journal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('id_item', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'hello', ['Journal'])


    def backwards(self, orm):
        # Deleting model 'Journal'
        db.delete_table(u'hello_journal')


    models = {
        u'hello.journal': {
            'Meta': {'object_name': 'Journal'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_item': ('django.db.models.fields.IntegerField', [], {}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'hello.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'other': ('django.db.models.fields.TextField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hello.requests': {
            'Meta': {'object_name': 'Requests'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'request_path': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']
