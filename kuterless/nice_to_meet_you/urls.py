from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import *
from api import MessagesList


urlpatterns = patterns('',
    url(r'scanned_user/', scanned_user, name='scanned_user'),
    
    url(r'view_cards/$', view_cards, name='view_cards'),
    
    url(r'scan_card/(?P<pk>[0-9]+)/$', scan_card, name='scan_card'),
    
    url(r'get_message/$', get_message, name='get_message'),

    url(r'get_latest_message/$', get_latest_message, name='get_latest_message'),
    
    url(r'message_board/$', message_board, name='message_board'),
    
    url(r'^api/get_messages/$', MessagesList.as_view(), name='api_messages_list'),

)


urlpatterns = format_suffix_patterns(urlpatterns)
    
    
    