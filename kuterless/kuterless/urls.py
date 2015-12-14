from django.conf.urls import patterns, include, url
from django.contrib import admin
from django_notify.urls import get_pattern as get_notify_pattern
from public_fulfillment.views import labs_root, about, root
from wiki.urls import get_pattern as get_wiki_pattern
from rest_framework.authtoken.views import  obtain_auth_token


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kuterless.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', root, name='home'),
    
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
        

)


urlpatterns += patterns('',
    (r'^notify/', get_notify_pattern()),
    (r'^wiki/', get_wiki_pattern())
)
