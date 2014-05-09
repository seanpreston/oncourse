# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .api import SchoolsListView, SchoolsView

urlpatterns = patterns(
    '',

    url(r'api/v0/schools/$', SchoolsListView.as_view(), name='api-v0-schools'),
    url(r'api/v0/schools/(?P<school_slug>[\w\d_.-]+)/$', SchoolsView.as_view(), name='api-v0-schools'),

)
