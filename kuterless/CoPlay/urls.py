from coplay import views
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'root/$', views.root, name='coplay_root'),
#/list
    url(r'list/$', views.IndexView.as_view(), name='discussions_list'),
#/add
    url(r'add/$', views.discussions_add, name='discussions_add'),
#pk (of discussion)/details
    url(r'^(?P<pk>\d+)/details/$', views.discussion_details, name='discussion_details'),
#pk (of discussion)/feedback_for
    url(r'^(?P<pk>\d+)/feedback/$', views.add_feedback, name='add_feedback'),
#pk (of discussion)/update_goals
    url(r'^(?P<pk>\d+)/update_goals/$', views.update_discussion, name='update_goals'),
#pk (of discussion)/add_decision
    url(r'^(?P<pk>\d+)/add_decision/$', views.add_decision, name='add_decision'),
#pk (of decision)/vote
    url(r'^(?P<pk>\d+)/vote/$', views.vote, name='vote'),

#pk (of discussion)/add_task
    url(r'^(?P<pk>\d+)/add_task/$', views.add_task, name='add_task'),

#pk (of task)/task_details
    url(r'^(?P<pk>\d+)/task_details/$', views.task_details, name='task_details'),    
#pk (of task)/update_task_description  
    url(r'^(?P<pk>\d+)/update_task_description/(?P<new_description>.+)/$', views.update_task_description, name='update_task_description'),
#pk (of task)/close_task
    url(r'^(?P<pk>\d+)/close_task/$', views.close_task, name='close_task'),        
)



    
    
    