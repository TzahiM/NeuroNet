# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AnonymousViewer'
        db.create_table(u'coplay_anonymousviewer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True, blank=True)),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coplay.Discussion'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('views_counter', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('views_counter_updated_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('discussion_updated_at_on_last_view', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'coplay', ['AnonymousViewer'])

        # Adding field 'UserProfile.a_player'
        db.add_column(u'coplay_userprofile', 'a_player',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Glimpse.anonymous_viewer'
        db.add_column(u'coplay_glimpse', 'anonymous_viewer',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['coplay.AnonymousViewer'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Glimpse.viewer'
        db.alter_column(u'coplay_glimpse', 'viewer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coplay.Viewer'], null=True))

    def backwards(self, orm):
        # Deleting model 'AnonymousViewer'
        db.delete_table(u'coplay_anonymousviewer')

        # Deleting field 'UserProfile.a_player'
        db.delete_column(u'coplay_userprofile', 'a_player')

        # Deleting field 'Glimpse.anonymous_viewer'
        db.delete_column(u'coplay_glimpse', 'anonymous_viewer_id')


        # Changing field 'Glimpse.viewer'
        db.alter_column(u'coplay_glimpse', 'viewer_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['coplay.Viewer']))

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
        u'coplay.anonymousviewer': {
            'Meta': {'object_name': 'AnonymousViewer'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']"}),
            'discussion_updated_at_on_last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'views_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'views_counter_updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'coplay.decision': {
            'Meta': {'object_name': 'Decision'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'coplay.discussion': {
            'Meta': {'object_name': 'Discussion'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_restricted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']"}),
            'feedbabk_type': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'coplay.followrelation': {
            'Meta': {'unique_together': "(('follower_user', 'following_user'),)", 'object_name': 'FollowRelation'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'follower_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follower_user'", 'to': u"orm['auth.User']"}),
            'following_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'following_user'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.glimpse': {
            'Meta': {'object_name': 'Glimpse'},
            'anonymous_viewer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['coplay.AnonymousViewer']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['coplay.Viewer']", 'null': 'True', 'blank': 'True'})
        },
        u'coplay.segment': {
            'Meta': {'object_name': 'Segment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.task': {
            'Meta': {'object_name': 'Task'},
            'closed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'closed_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'final_state': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'goal_description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']", 'null': 'True', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'a_player': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_limit_discussion_access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_limit_discussion_to_login_users_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recieve_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recieve_updates': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Segment']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'coplay.userupdate': {
            'Meta': {'object_name': 'UserUpdate'},
            'already_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']", 'null': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipient'", 'to': u"orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'applicabale_sender'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.viewer': {
            'Meta': {'object_name': 'Viewer'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']"}),
            'discussion_updated_at_on_last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_a_follower': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'views_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'views_counter_updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'coplay.vote': {
            'Meta': {'unique_together': "(('voater', 'decision'),)", 'object_name': 'Vote'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'decision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Decision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'voater': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['coplay']