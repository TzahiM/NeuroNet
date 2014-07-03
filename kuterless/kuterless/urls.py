from public_fulfillment.views import root
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django_notify.urls import get_pattern as get_notify_pattern
from public_fulfillment.views import labs_root, about
from wiki.urls import get_pattern as get_wiki_pattern


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
    
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name="login"),

    url(r'^alogout/$',
        'django.contrib.auth.views.logout',
        name="logout"),
                       
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    
    
)


urlpatterns += patterns('',
    (r'^notify/', get_notify_pattern()),
    (r'^wiki/', get_wiki_pattern())
)
