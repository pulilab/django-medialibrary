# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Shelf.meta'
        db.add_column(u'medialibrary_shelf', 'meta',
                      self.gf('jsonfield.fields.JSONField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Shelf.meta'
        db.delete_column(u'medialibrary_shelf', 'meta')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'medialibrary.audio': {
            'Meta': {'object_name': 'Audio'},
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'application/octet-stream'", 'max_length': '50', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'default': "'original'", 'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.Shelf']"})
        },
        u'medialibrary.audioshelf': {
            'Meta': {'object_name': 'AudioShelf', '_ormbases': [u'medialibrary.Shelf']},
            u'shelf_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['medialibrary.Shelf']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'medialibrary.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'application/octet-stream'", 'max_length': '50', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'default': "'original'", 'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.Shelf']"})
        },
        u'medialibrary.imageshelf': {
            'Meta': {'object_name': 'ImageShelf', '_ormbases': [u'medialibrary.Shelf']},
            u'shelf_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['medialibrary.Shelf']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'medialibrary.medialibrary': {
            'Meta': {'object_name': 'MediaLibrary'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'medialibrary.shelf': {
            'Meta': {'object_name': 'Shelf'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.MediaLibrary']"}),
            'meta': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2', 'db_index': 'True'})
        },
        u'medialibrary.shelfrelation': {
            'Meta': {'object_name': 'ShelfRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationships'", 'to': u"orm['medialibrary.Shelf']"})
        },
        u'medialibrary.video': {
            'Meta': {'object_name': 'Video'},
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'application/octet-stream'", 'max_length': '50', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'default': "'original'", 'max_length': '255', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.Shelf']"}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'medialibrary.videoshelf': {
            'Meta': {'object_name': 'VideoShelf', '_ormbases': [u'medialibrary.Shelf']},
            u'shelf_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['medialibrary.Shelf']", 'unique': 'True', 'primary_key': 'True'}),
            'thumbnails': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['medialibrary.ImageShelf']", 'null': 'True', 'through': u"orm['medialibrary.VideoThumbnail']", 'blank': 'True'})
        },
        u'medialibrary.videothumbnail': {
            'Meta': {'object_name': 'VideoThumbnail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.ImageShelf']"}),
            'selected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.VideoShelf']"})
        }
    }

    complete_apps = ['medialibrary']