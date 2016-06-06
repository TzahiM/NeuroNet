# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KuterLessApp'
        db.create_table(u'coplay_kuterlessapp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('app_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'coplay', ['KuterLessApp'])

        # Adding field 'Discussion.picture'
        db.add_column(u'coplay_discussion', 'picture',
                      self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=50000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Discussion.anyway_progress_status'
        db.add_column(u'coplay_discussion', 'anyway_progress_status',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Discussion.anyway_discuss_id'
        db.add_column(u'coplay_discussion', 'anyway_discuss_id',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Discussion.movie_url'
        db.add_column(u'coplay_discussion', 'movie_url',
                      self.gf('django.db.models.fields.URLField')(default=None, max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Discussion.movie_url_url_text'
        db.add_column(u'coplay_discussion', 'movie_url_url_text',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.application'
        db.add_column(u'coplay_userprofile', 'application',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coplay.KuterLessApp'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.application_specific_id'
        db.add_column(u'coplay_userprofile', 'application_specific_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'KuterLessApp'
        db.delete_table(u'coplay_kuterlessapp')

        # Deleting field 'Discussion.picture'
        db.delete_column(u'coplay_discussion', 'picture')

        # Deleting field 'Discussion.anyway_progress_status'
        db.delete_column(u'coplay_discussion', 'anyway_progress_status')

        # Deleting field 'Discussion.anyway_discuss_id'
        db.delete_column(u'coplay_discussion', 'anyway_discuss_id')

        # Deleting field 'Discussion.movie_url'
        db.delete_column(u'coplay_discussion', 'movie_url')

        # Deleting field 'Discussion.movie_url_url_text'
        db.delete_column(u'coplay_discussion', 'movie_url_url_text')

        # Deleting field 'UserProfile.application'
        db.delete_column(u'coplay_userprofile', 'application_id')

        # Deleting field 'UserProfile.application_specific_id'
        db.delete_column(u'coplay_userprofile', 'application_specific_id')


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
        u'coplay.anonymousvisitor': {
            'Meta': {'object_name': 'AnonymousVisitor'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'coplay.anonymousvisitorviewer': {
            'Meta': {'object_name': 'AnonymousVisitorViewer'},
            'anonymous_visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.AnonymousVisitor']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']"}),
            'discussion_updated_at_on_last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'anyway_discuss_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'anyway_progress_status': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_restricted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_viewing_require_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Location']", 'null': 'True', 'blank': 'True'}),
            'location_desc': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'locked_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'movie_url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'movie_url_url_text': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'parent_url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'parent_url_text': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '50000', 'null': 'True', 'blank': 'True'}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'voice_recording': ('django.db.models.fields.files.FileField', [], {'max_length': '5000000', 'null': 'True', 'blank': 'True'})
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
            'anonymous_visitor_viewer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['coplay.AnonymousVisitorViewer']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['coplay.Viewer']", 'null': 'True', 'blank': 'True'})
        },
        u'coplay.kuterlessapp': {
            'Meta': {'object_name': 'KuterLessApp'},
            'app_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'\\u05d9\\u05e9\\u05e8\\u05d0\\u05dc'", 'max_length': '20', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'coplay.segment': {
            'Meta': {'object_name': 'Segment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.taggeddiscussions': {
            'Meta': {'object_name': 'TaggedDiscussions'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Discussion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'coplay_taggeddiscussions_items'", 'to': u"orm['taggit.Tag']"})
        },
        u'coplay.taggedusers': {
            'Meta': {'object_name': 'TaggedUsers'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'coplay_taggedusers_items'", 'to': u"orm['taggit.Tag']"})
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
            'result_picture': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '50000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'coplay.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'a_player': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.KuterLessApp']", 'null': 'True', 'blank': 'True'}),
            'application_specific_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'can_limit_discussion_access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_limit_discussion_to_login_users_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coplay.Location']", 'null': 'True', 'blank': 'True'}),
            'location_desc': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recieve_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recieve_updates': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['coplay']