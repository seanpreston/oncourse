# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_settings.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),

    # API v0
    url(r'^', include('api_urls')),

    # Index
    # url(r'^$', 'project_settings.views.home', name='home'),

)
