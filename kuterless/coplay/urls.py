from coplay import views, api
from coplay.api import create_feedback_view, AddFeedBackView, create_task_view, \
    create_discussion_view
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
    url(r'root/$', views.root, name='coplay_root'),
#/list
#     url(r'list/$', views.IndexView.as_view(), name='discussions_list'),
    url(r'list/$', views.discussion_tag_list, name='discussions_list'),
#/list
    url(r'^discussion_tag_list/(?P<pk>[0-9]+)/$', views.discussion_tag_list, name='discussion_tag_list'),

    url(r'^discussion_url_list/$', views.discussion_url_list, name='discussion_url_list'),
    
    url(r'^add_on_discussion_url_list/$', views.add_on_discussion_url_list, name='add_on_discussion_url_list'),

#/add
    url(r'add/$', views.add_discussion, name='add_discussion'),

    url(r'add_with_tag/(?P<pk>[0-9]+)/$', views.add_discussion, name='add_with_tag'),

# http://127.0.0.1:8000/labs/coplay/add_on_add_with_url/?parent_url=http://www.ynet.co.il/articles/0,7340,L-4722534,00.html&parent_url_text=hi hi
    url(r'add_on_add_with_url/$', views.add_on_add_discussion, name='add_on_add_with_url'),
    
# http://127.0.0.1:8000/labs/coplay/add_with_url/?parent_url=http://www.ynet.co.il/articles/0,7340,L-4722534,00.html&parent_url_text=hi hi
    url(r'add_with_url/$', views.add_discussion, name='add_with_url'),


#pk (of discussion)/details
    url(r'^(?P<pk>\d+)/details/$', views.discussion_details, name='discussion_details'),
    url(r'^(?P<pk>\d+)/update/$', views.UpdateDiscussionDescView.as_view(), name='discussion_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteDiscussionView.as_view(success_url='discussions_list'), name='discussion_delete'),
    
#pk (of discussion)/start_follow
    url(r'^(?P<pk>\d+)/start_follow/$', views.start_follow, name='start_follow'),
    
#pk (of discussion)/stop_follow
    url(r'^(?P<pk>\d+)/stop_follow/$', views.stop_follow, name='stop_follow'),

#pk (of discussion)/delete_discussion
    url(r'^(?P<pk>\d+)/delete_discussion/$', views.delete_discussion, name='delete_discussion'),
#pk (of decision)/vote
    url(r'^(?P<pk>\d+)/vote/$', views.vote, name='vote'),

#pk (of discussion)/add_task
    url(r'^(?P<pk>\d+)/create-decision/$', views.CreateDecisionView.as_view(), name='create_decision'),
    url(r'^(?P<pk>\d+)/create-feedback/$', views.CreateFeedbackView.as_view(), name='create_feedback'),
    url(r'^(?P<pk>\d+)/create-task/$', views.CreateTaskView.as_view(), name='create_task'),

#pk (of task)/task_details
    url(r'^(?P<pk>\d+)/task_details/$', views.task_details, name='task_details'),
#pk (of task)/update_task_description
    url(r'^(?P<pk>\d+)/update_task/$', views.update_task_description, name='update_task_status_description'),
#pk (of task)/close_task
    url(r'^(?P<pk>\d+)/close_task/$', views.close_task, name='close_task'),
#pk (of task)/abort_task
    url(r'^(?P<pk>\d+)/abort_task/$', views.abort_task, name='abort_task'),
#pk (of task)/re_open_task
    url(r'^(?P<pk>\d+)/re_open_task/$', views.re_open_task, name='re_open_task'),
#/username/user_coplay_report
# ex: labs/coplay/Tzahim/user_coplay_report
    url(r'^(?P<username>.+)/user_coplay_report/$', views.user_coplay_report, name='user_coplay_report'),
    
# ex: labs/coplay/Tzahim/start_follow_user
    url(r'^(?P<username>.+)/start_follow_user/$', views.start_follow_user, name='start_follow_user'),
    
   url(r'^user_update_details/(?P<pk>[0-9]+)/$', views.user_update_details, name='user_update_details'),

   url(r'^user_update_mark_recipient_read/(?P<pk>[0-9]+)/$', views.user_update_mark_recipient_read, name='user_update_mark_recipient_read'),
    
    url(r'^start_follow_tag/(?P<pk>[0-9]+)/$', views.start_follow_tag, name='start_follow_tag'),

    url(r'^stop_follow_tag/(?P<pk>[0-9]+)/$', views.stop_follow_tag, name='stop_follow_tag'),
    
# ex: labs/coplay/Tzahim/stop_follow_user
    url(r'^(?P<username>.+)/stop_follow_user/$', views.stop_follow_user, name='stop_follow_user'),

    url(r'^api/discussions/$', api.DiscussionList.as_view(), name='api_discussions_list'),

    url(r'^api/discussion/(?P<pk>[0-9]+)/$', api.DiscussionDetails.as_view(), name='api_discussion'),

    url(r'^api/users/$', api.UserList.as_view(), name='api_users_list'),
    url(r'^api/user/(?P<pk>[0-9]+)/$', api.UserDetails.as_view(), name='api_user'),

    url(r'^api/feedbacks/$', api.FeedbackList.as_view(), name='api_feedbacks_list'),
    url(r'^api/feedback/(?P<pk>[0-9]+)/$', api.FeedbackDetails.as_view(), name='api_feedback'),


    url(r'^api/decisions/$', api.DecisionList.as_view(), name='api_decisions_list'),
    url(r'^api/decision/(?P<pk>[0-9]+)/$', api.DecisionDetails.as_view(), name='api_decision'),
    
    url(r'^api/votes/$', api.VoteList.as_view(), name='api_votes_list'),
    url(r'^api/vote/(?P<pk>[0-9]+)/$', api.VoteDetails.as_view(), name='api_vote'),

    url(r'^api/tasks/$', api.TaskList.as_view(), name='api_tasks_list'),
    url(r'^api/task/(?P<pk>[0-9]+)/$', api.TaskDetails.as_view(), name='api_task'),


    url(r'^api/viewers/$', api.ViewerList.as_view(), name='api_viewers_list'),
    url(r'^api/viewer/(?P<pk>[0-9]+)/$', api.ViewerDetails.as_view(), name='api_viewer'),


    url(r'^api/anonymousvisitors/$', api.AnonymousVisitorList.as_view(), name='api_anonymousvisitors_list'),
    url(r'^api/anonymousvisitor/(?P<pk>[0-9]+)/$', api.AnonymousVisitorDetails.as_view(), name='api_anonymousvisitor'),


    url(r'^api/anonymousvisitorvviewers/$', api.AnonymousVisitorViewerList.as_view(), name='api_anonymousvisitorvviewers_list'),
    url(r'^api/anonymousvisitorvviewer/(?P<pk>[0-9]+)/$', api.AnonymousVisitorViewerDetails.as_view(), name='api_anonymousvisitorvviewer'),


    url(r'^api/glimpses/$', api.GlimpseList.as_view(), name='api_glimpses_list'),
    url(r'^api/glimpse/(?P<pk>[0-9]+)/$', api.GlimpseDetails.as_view(), name='api_glimpse'),


    url(r'^api/followrelations/$', api.FollowRelationList.as_view(), name='api_s_list'),
    url(r'^api/followrelation/(?P<pk>[0-9]+)/$', api.FollowRelationDetails.as_view(), name='api_'),


    url(r'^api/userprofiles/$', api.UserProfileList.as_view(), name='api_userprofiles_list'),
    url(r'^api/userprofile/(?P<pk>[0-9]+)/$', api.UserProfileDetails.as_view(), name='api_userprofile'),


    url(r'^api/userupdates/$', api.UserUpdateList.as_view(), name='api_userupdates_list'),

    url(r'^api/userupdates/unread/$', api.UserUpdateListUnRead.as_view(), name='api_userupdates_list_unread'),
    
    url(r'^api/userupdate/(?P<pk>[0-9]+)/$', api.UserUpdateDetails.as_view(), name='api_userupdate'),

    url(r'^api/userupdate/read_notification/(?P<pk>[0-9]+)/$', api.userupdate_read_notification, name='api_userupdate_read_notification'),


    url(r'^api/decision_whole/(?P<pk>[0-9]+)/$', api.DecisionWhole.as_view(), name='api_decision_whole'),
    
    url(r'^api/discussion_whole/(?P<pk>[0-9]+)/$', api.DiscussionWhole.as_view(), name='api_discussion_whole'),
    
    url(r'^api/example_view/$', api.example_view, name='api_example_view'),

    url(r'^api/create_feedback/(?P<pk>[0-9]+)/$', create_feedback_view, name='api_create_feedback'),
    
    url(r'^api/create_task/(?P<pk>[0-9]+)/$', create_task_view, name='api_create_task'),
    
    url(r'^api/create_discussion/$', create_discussion_view, name='api_create_discussion'),
    
)


urlpatterns = format_suffix_patterns(urlpatterns)
    
    
    