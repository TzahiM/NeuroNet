# Generated by Django 2.2.7 on 2020-02-11 18:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousVisitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnonymousVisitorViewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views_counter', models.IntegerField(default=0)),
                ('views_counter_updated_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('discussion_updated_at_on_last_view', models.DateTimeField(blank=True, default=None, null=True)),
                ('anonymous_visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.AnonymousVisitor')),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(2000)], verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('locked_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('description_updated_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_restricted', models.BooleanField(default=False)),
                ('is_viewing_require_login', models.BooleanField(default=False)),
                ('latitude', models.FloatField(blank=True, default=None, null=True)),
                ('longitude', models.FloatField(blank=True, default=None, null=True)),
                ('location_desc', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('parent_url', models.URLField(blank=True, default=None, max_length=2000, null=True)),
                ('parent_url_text', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('picture', models.ImageField(blank=True, default=None, max_length=50000, null=True, upload_to='uploads/%Y/%m/%d/')),
                ('anyway_progress_status', models.IntegerField(blank=True, default=None, null=True)),
                ('anyway_discuss_id', models.IntegerField(blank=True, default=None, null=True)),
                ('movie_url', models.URLField(blank=True, default=None, max_length=2000, null=True)),
                ('movie_url_url_text', models.CharField(blank=True, default=None, max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KuterLessApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=200, verbose_name='title')),
                ('app_description', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(2000)])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('street', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('state', models.CharField(blank=True, default='ישראל', max_length=20)),
                ('latitude', models.FloatField(blank=True, default=None, null=True)),
                ('longitude', models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='שם')),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(2000)], verbose_name='תאור')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views_counter', models.IntegerField(default=0)),
                ('views_counter_updated_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('discussion_updated_at_on_last_view', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_a_follower', models.BooleanField(default=False)),
                ('is_invited', models.BooleanField(default=False)),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.Discussion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=200)),
                ('content', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(2000)])),
                ('details_url', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('already_read', models.BooleanField(default=False)),
                ('discussion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coplay.Discussion')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applicabale_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recieve_notifications', models.BooleanField(default=True)),
                ('recieve_updates', models.BooleanField(default=True)),
                ('can_limit_discussion_access', models.BooleanField(default=False)),
                ('can_limit_discussion_to_login_users_only', models.BooleanField(default=False)),
                ('a_player', models.BooleanField(default=False)),
                ('latitude', models.FloatField(blank=True, default=None, null=True)),
                ('longitude', models.FloatField(blank=True, default=None, null=True)),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(2000)], verbose_name='Description')),
                ('location_desc', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('application_specific_id', models.IntegerField(blank=True, default=0)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coplay.KuterLessApp')),
                ('followed_discussions_tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coplay.Location')),
                ('segment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coplay.Segment')),
                ('user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_description', models.TextField(validators=[django.core.validators.MaxLengthValidator(2000)])),
                ('target_date', models.DateTimeField()),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('status_description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'פעילה'), (2, 'הושלמה בהצלחה'), (3, 'פוספסה'), (4, 'בוטלה בזמן')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('final_state', models.BooleanField(default=False)),
                ('result_picture', models.ImageField(blank=True, default=None, max_length=50000, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='תמונה של התוצאה')),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='closed_by', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coplay.Discussion')),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaggedUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.UserProfile')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coplay_taggedusers_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedDiscussions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.Discussion')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coplay_taggeddiscussions_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Glimpse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('anonymous_visitor_viewer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='coplay.AnonymousVisitorViewer')),
                ('viewer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='coplay.Viewer')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedbabk_type', models.IntegerField(choices=[(1, 'עידוד'), (2, 'שיתוף פעולה'), (3, 'אינטואיציה'), (4, 'עצה')], verbose_name='סוג התגובה')),
                ('content', models.TextField(validators=[django.core.validators.MaxLengthValidator(2000)], verbose_name='תוכן התגובה')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('voice_recording', models.FileField(blank=True, max_length=5000000, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='הקלטה')),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.Discussion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='discussion',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coplay.Location'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(validators=[django.core.validators.MaxLengthValidator(2000)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.Discussion')),
            ],
        ),
        migrations.AddField(
            model_name='anonymousvisitorviewer',
            name='discussion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.Discussion'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.IntegerField(choices=[(5, 'רעיון מצוייו'), (4, 'טוב מאוד'), (3, 'לא רע'), (2, 'אין דעה'), (1, 'רעיון לא טוב')])),
                ('decision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coplay.Decision')),
                ('voater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('voater', 'decision')},
            },
        ),
        migrations.CreateModel(
            name='FollowRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('follower_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_user', to=settings.AUTH_USER_MODEL)),
                ('following_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('follower_user', 'following_user')},
            },
        ),
    ]