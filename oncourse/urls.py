# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

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

    # Index
    # url(r'^$', 'project_settings.views.home', name='home'),

)
