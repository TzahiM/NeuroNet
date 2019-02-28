from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import serve
from django_notify.urls import get_pattern as get_notify_pattern
from kuterless.settings import MEDIA_ROOT
from public_fulfillment.views import labs_root, about, root
from rest_framework.authtoken.views import obtain_auth_token
from wiki.urls import get_pattern as get_wiki_pattern
from django.http.response import HttpResponse, HttpResponseRedirect
#from gtts import gTTS




admin.autodiscover()

#127.0.0.1:8000/redirect_neuronet/?name=HTML5 has added some new attributes, and several HTML 4.01 attributes are removed from HTML5
def messages_rx(request):
    name = request.REQUEST.get('name', '')
#    tts = gTTS(text='My name is ' + name + '. Nice to meet you.', lang='en', slow=False)
#    tts = gTTS(text=name, lang='en', slow=False)
#    tts.save("media/zzz.mp3")

    return HttpResponseRedirect('https://eventbuzz.co.il/neuronet1')

def redirect_neuronet(request):
    name = request.REQUEST.get('name', '')
#    tts = gTTS(text='My name is ' + name + '. Nice to meet you.', lang='en', slow=False)
#    tts = gTTS(text=name, lang='en', slow=False)
#    tts.save("media/zzz.mp3")


def redirect_neuronet_tzahi_manistersky(request):
#    name = request.REQUEST.get('name', '')
#    tts = gTTS(text='My name is ' + name + '. Nice to meet you.', lang='en', slow=False)
#    tts = gTTS(text=name, lang='en', slow=False)
#    tts.save("media/zzz.mp3")

    return HttpResponseRedirect('https://www.facebook.com/Tzahiman')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kuterless.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', root, name='home'),
    
    url(r'^messages_rx/', messages_rx, name="messages_rx" ),
    
    url(r'^redirect_neuronet/tzahi.manistersky', redirect_neuronet_tzahi_manistersky, name="redirect_neuronet_tzahi_manistersky" ),
    
    url(r'^redirect_neuronet/', redirect_neuronet, name="redirect_neuronet" ),
    
    url(r'^ntmu/', include('nice_to_meet_you.urls', namespace="nice_to_meet_you")),
        
    url(r'^public_fulfillment/', include('public_fulfillment.urls', namespace="public_fulfillment")),

    url(r'^labs/$', labs_root , name = "labs_root"),

    url(r'^labs/coplay/', include('coplay.urls', namespace="coplay")),
    
    url(r'^labs/memecache/', include('memecache.urls', namespace="memecache")),
    
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name="login"),

    url(r'^alogout/$',
        'django.contrib.auth.views.logout',
        name="logout"),
                       
    url(r'^password_reset/', include('password_reset.urls')),
                            
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
       
    url(r'^api-token-auth/', obtain_auth_token),
        
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT,}),
)


urlpatterns += patterns('',
    (r'^notify/', get_notify_pattern()),
    (r'^wiki/', get_wiki_pattern())
)
