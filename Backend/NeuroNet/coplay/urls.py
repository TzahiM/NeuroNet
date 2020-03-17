from coplay import views, api
from coplay.api import create_feedback_view, AddFeedBackView, create_task_view, \
    create_discussion_view
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('root/', views.root, name="coplay_root"),
    path('list/', views.discussion_tag_list, name="discussions_list"),
    path('discussion_tag_list/<int:pk>/', views.discussion_tag_list, name="discussion_tag_list"),
    path('discussion_url_list/', views.discussion_url_list, name="discussion_url_list"),
    path('add_on_discussion_url_list/', views.add_on_discussion_url_list, name="add_on_discussion_url_list"),
    path('related_discussions_of_url/', views.related_discussions_of_url, name="related_discussions_of_url"),
    path('add/', views.add_discussion, name="add_discussion"),
    path('add_with_tag/<int:pk>/', views.add_discussion, name="add_with_tag"),
    path('add_on_add_with_url/', views.add_on_add_discussion, name="add_on_add_with_url"),
    path('<int:pk>/discussion_details/', views.discussion_details, name='discussion_details'),
    path('<int:pk>/update/', views.UpdateDiscussionDescView.as_view(), name="discussion_update"),
    path('<int:pk>/delete/', views.DeleteDiscussionView.as_view(success_url='discussions_list'), name="discussion_delete"),
    path('<int:pk>/start_follow/', views.start_follow, name="start_follow"),
    path('<int:pk>/stop_follow/', views.stop_follow,   name="stop_follow"),
    path('<int:pk>/vote/', views.vote, name="vote"),
    path('<int:pk>/create-decision/', views.CreateDecisionView.as_view(), name="create_decision"),
    path('<int:pk>/create-feedback/', views.CreateFeedbackView.as_view(), name="create_feedback"),
    path('<int:pk>/create-task/', views.CreateTaskView.as_view(),         name="create_task"),
    path('<int:pk>/task_details/', views.task_details,                    name="task_details"),
    path('<int:pk>/update_task/', views.update_task_description,          name="update_task_status_description"),
    path('<int:pk>/abort_task/', views.abort_task,                        name="abort_task"),
    path('<int:pk>/close_task/', views.close_task,                        name="close_task"),
    path('<int:pk>/re_open_task/', views.re_open_task,                    name="re_open_task"),
    path('<str:username>/user_coplay_report/', views.user_coplay_report,  name="user_coplay_report"),
    path('<str:username>/start_follow_user/', views.start_follow_user,    name="start_follow_user"),
    path('<str:username>/stop_follow_user/', views.stop_follow_user,      name="stop_follow_user"),
    path('user_update_details/<int:pk>/', views.user_update_details,      name="user_update_details"),
    path('user_update_mark_recipient_read/<int:pk>/', views.user_update_mark_recipient_read, name="user_update_mark_recipient_read"),
    path('start_follow_tag/<int:pk>/', views.start_follow_tag,                               name="start_follow_tag"),
    path('stop_follow_tag/<int:pk>/', views.stop_follow_tag,                                 name="stop_follow_tag"),

    path('api/discussions/', api.DiscussionList.as_view(), "api_discussions_list"),
    path('api/discussion/<int:pk>/', api.DiscussionList.as_view(), "api_discussion"),
    path('api/users/', api.UserList.as_view(), "api_users_list"),
    path('api/user/<int:pk>/', api.UserList.as_view(), "api_user"),
    path('api/feedbacks/', api.FeedbackList.as_view(), "api_feedbacks_list"),
    path('api/feedback/<int:pk>/', api.FeedbackList.as_view(), "api_feedback"),
    path('api/decisions/', api.DecisionList.as_view(), "api_decisions_list"),
    path('api/decision/<int:pk>/', api.DecisionList.as_view(), "api_decision"),
    path('api/votes/', api.VoteList.as_view(), "api_votes_list"),
    path('api/vote/<int:pk>/', api.VoteList.as_view(), "api_vote"),
    path('api/tasks/', api.TaskList.as_view(), "api_tasks_list"),
    path('api/task/<int:pk>/', api.TaskList.as_view(), "api_task"),
    path('api/viewers/', api.ViewerList.as_view(), "api_viewers_list"),
    path('api/viewer/<int:pk>/', api.ViewerList.as_view(), "api_viewers_list"),
    path('api/anonymousvisitors/', api.AnonymousVisitorList.as_view(), "api_anonymousvisitors_list"),
    path('api/anonymousvisitor/<int:pk>/', api.AnonymousVisitorList.as_view(), "api_anonymousvisitor"),
    path('api/anonymousvisitorvviewers/', api.AnonymousVisitorViewerList.as_view(), "api_anonymousvisitorvviewers_list"),
    path('api/anonymousvisitorvviewer/<int:pk>/', api.AnonymousVisitorViewerList.as_view(), "api_anonymousvisitorvviewer"),
    path('api/glimpses/', api.GlimpseList.as_view(), "api_glimpses_list"),
    path('api/glimpse/<int:pk>/', api.GlimpseList.as_view(), "api_glimpse"),
    path('api/followrelations/', api.FollowRelationList.as_view(), "api_followers_list"),
    path('api/followrelation/<int:pk>/', api.FollowRelationList.as_view(), "api_follower"),
    path('api/userprofiles/', api.UserProfileList.as_view(), "api_userprofiles_list"),
    path('api/userprofile/<int:pk>/', api.UserProfileList.as_view(), "api_userprofile"),
    path('api/userupdates/', api.UserUpdateList.as_view(), "api_userupdates_list"),
    path('api/userupdates/unread/', api.UserUpdateListUnRead.as_view(), "api_userupdates_list_unread"),
    path('api/userupdates/all/', api.UserUpdateListAll.as_view(), "api_userupdates_list_all"),
    path('api/userupdate/read_notification/<int:pk>/', api.userupdate_read_notification, "api_userupdate_read_notification"),
    path('api/decision_whole/<int:pk>/', api.DecisionWhole.as_view(), "api_decision_whole"),
    path('api/discussion_whole/<int:pk>/', api.DiscussionWhole.as_view(), "api_discussion_whole"),
    path('api/example_view/', api.example_view, "api_example_view"),
    path('api/create_feedback/<int:pk>/', create_feedback_view, "api_create_feedback"),
    path('api/create_task/<int:pk>/', create_task_view, "api_create_task"),
    path('api/create_discussion/', create_discussion_view, "api_create_discussion"),
]


urlpatterns = format_suffix_patterns(urlpatterns)
    
    
    