from coplay import urls
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy, reverse
from public_fulfillment.views import home, labs_root


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kuterless.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', labs_root, name='home'),
    
    url(r'^public_fulfillment/', include('public_fulfillment.urls', namespace="public_fulfillment")),

    url(r'^labs/$', labs_root , name = "labs_root"),

    url(r'^labs/coplay/', include('coplay.urls', namespace="coplay")),
    
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name="login"),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': 'home'}, name="logout"),
    
    
    
)
