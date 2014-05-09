# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .api import SchoolsListView

urlpatterns = patterns(
    '',

    url(r'api/v0/schools/$', SchoolsListView.as_view(), name='api-v0-schools'),

)
