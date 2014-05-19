# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.views import logout_then_login

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_settings.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),

    # API Proxy
    # url(r'^site-api-(?P<api>0|1|public|public-1)/', include('oncourse.api-proxy.urls')),

    # API v0
    url(r'^', include('oncourse.api_urls')),

    # Dash
    url(r'^dash/$', 'oncourse.views.dash', name='dash'),

    # Login
    url(r'^login/$', 'oncourse.views.login', name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),

    # Payments
    url(r'^', include('oncourse.payments.urls')),

    # Registration
    url(r'^', include('oncourse.registration.urls')),

    # Landing
    url(r'^$', 'oncourse.views.landing', name='landing'),

)
# ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
