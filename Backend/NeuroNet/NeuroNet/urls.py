"""
NeuroNet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from public_fulfillment.views import labs_root, about, root
from django.contrib.auth.views import LoginView, LogoutView
from public_fulfillment import forms
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', root, name="home"),
    path('ntmu/', include(('nice_to_meet_you.urls', "nice_to_meet_you"), "nice_to_meet_you")),
    path('labs/coplay/', include(('coplay.urls', 'coplay'), 'coplay')),
    path('labs/memecache/', include(('memecache.urls', "memecache"), "memecache")),
    path('public_fulfillment/', include(('public_fulfillment.urls', "public_fulfillment"), "public_fulfillment")),
    path('labs/', labs_root, name="labs_root"),
    path('login/',
        LoginView.as_view
        (
            template_name='login.html',
            authentication_form=forms.BootstrapAuthenticationForm,
            redirect_authenticated_user = True,
            #extra_context=
            #{
            #    'title': 'Log in',
            #    'year' : datetime.now().year,
            #}
        ),
    name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('password_reset/', include(('password_reset.urls', "password_reset"), "password_reset")),
    path('api-auth/', include(('rest_framework.urls', "rest_framework"), "rest_framework")),
    path('api-token-auth/', obtain_auth_token, name='obtain_auth_token'),

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)