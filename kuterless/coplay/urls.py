from coplay import views
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
    url(r'root/$', views.root, name='coplay_root'),
#/list
    url(r'list/$', views.IndexView.as_view(), name='discussions_list'),
#/add
    url(r'add/$', views.add_discussion, name='add_discussion'),
#pk (of discussion)/details
    url(r'^(?P<pk>\d+)/details/$', views.discussion_details, name='discussion_details'),
    url(r'^(?P<pk>\d+)/update/$', views.UpdateDiscussionDescView.as_view(), name='discussion_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteDiscussionView.as_view(success_url='discussions_list'), name='discussion_delete'),
    
#pk (of discussion)/start_follow
    url(r'^(?P<pk>\d+)/start_follow/$', views.start_follow, name='start_follow'),
    
#pk (of discussion)/stop_follow
    url(r'^(?P<pk>\d+)/stop_follow/$', views.stop_follow, name='stop_follow'),

#pk (of discussion)/feedback_for
    url(r'^(?P<pk>\d+)/feedback/$', views.add_feedback, name='add_feedback'),
#pk (of discussion)/update_goals
    url(r'^(?P<pk>\d+)/update_goals/$', views.update_discussion, name='update_goals'),
#pk (of discussion)/delete_discussion
    url(r'^(?P<pk>\d+)/delete_discussion/$', views.delete_discussion, name='delete_discussion'),
#pk (of discussion)/add_decision
    url(r'^(?P<pk>\d+)/add_decision/$', views.add_decision, name='add_decision'),
#pk (of decision)/vote
    url(r'^(?P<pk>\d+)/vote/$', views.vote, name='vote'),

#pk (of discussion)/add_task
    url(r'^(?P<pk>\d+)/create-decision/$', views.CreateDecisionView.as_view(), name='create_decision'),
    url(r'^(?P<pk>\d+)/create-feedback/$', views.CreateFeedbackView.as_view(), name='create_feedback'),
    url(r'^(?P<pk>\d+)/create-task/$', views.CreateTaskView.as_view(), name='create_task'),
    url(r'^(?P<pk>\d+)/add_task/$', views.add_task, name='add_task'),

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
    
    


)



    
    
    