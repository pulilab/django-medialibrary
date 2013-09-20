# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VideoThumbnail'
        db.create_table('medialibrary_videothumbnail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medialibrary.VideoShelf'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medialibrary.ImageShelf'])),
            ('selected', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('medialibrary', ['VideoThumbnail'])


    def backwards(self, orm):
        # Deleting model 'VideoThumbnail'
        db.delete_table('medialibrary_videothumbnail')


    models = {
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
        'medialibrary.audio': {
            'Meta': {'object_name': 'Audio'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'default': "'original'", 'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['medialibrary.Shelf']"})
        },
        'medialibrary.audioshelf': {
            'Meta': {'object_name': 'AudioShelf', '_ormbases': ['medialibrary.Shelf']},
            'shelf_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['medialibrary.Shelf']", 'unique': 'True', 'primary_key': 'True'})
        },
        'medialibrary.image': {
            'Meta': {'object_name': 'Image'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'default': "'original'", 'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['medialibrary.Shelf']"})
        },
        'medialibrary.imageshelf': {
            'Meta': {'object_name': 'ImageShelf', '_ormbases': ['medialibrary.Shelf']},
            'shelf_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['medialibrary.Shelf']", 'unique': 'True', 'primary_key': 'True'})
        },
        'medialibrary.medialibrary': {
            'Meta': {'object_name': 'MediaLibrary'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'medialibrary.shelf': {
            'Meta': {'object_name': 'Shelf'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['medialibrary.MediaLibrary']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2', 'db_index': 'True'})
        },
        'medialibrary.shelfrelation': {
            'Meta': {'object_name': 'ShelfRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationships'", 'to': "orm['medialibrary.Shelf']"})
        },
        'medialibrary.video': {
            'Meta': {'object_name': 'Video'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'default': "'original'", 'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['medialibrary.Shelf']"})
        },
        'medialibrary.videoshelf': {
            'Meta': {'object_name': 'VideoShelf', '_ormbases': ['medialibrary.Shelf']},
            'shelf_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['medialibrary.Shelf']", 'unique': 'True', 'primary_key': 'True'}),
            'thumbnails': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['medialibrary.ImageShelf']", 'null': 'True', 'through': "orm['medialibrary.VideoThumbnail']", 'blank': 'True'})
        },
        'medialibrary.videothumbnail': {
            'Meta': {'object_name': 'VideoThumbnail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['medialibrary.ImageShelf']"}),
            'selected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['medialibrary.VideoShelf']"})
        }
    }

    complete_apps = ['medialibrary']