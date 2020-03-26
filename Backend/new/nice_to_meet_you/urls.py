from django.urls import path
from .views import *
#from .api import MessagesList



urlpatterns = [
    #path('', home, name='home'),
    path('scanned_user/',scanned_user,name='scanned_user'),
    path('view_cards/',view_cards,name='view_cards'),
    path('scan_card/<int:pk>/', scan_card, name='scan_card'),
    path('view_card/<int:pk>/', view_card, name='view_card'),
    path('get_message/',get_message,name='get_message'),
    path('get_latest_message/',get_latest_message,name='get_latest_message'),
    path('message_board/',message_board,name='message_board'),
    path('scoring_board/',scoring_board,name='scoring_board'),
    path('scoring_clear/',scoring_clear,name='scoring_clear'),
    #path('api/get_messages/',MessagesList.as_view(),name='api_messages_list'),

]
