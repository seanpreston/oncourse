# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',

    # URLs
    url(r'^', include('schools.api_urls')),
    url(r'^', include('subjects.api_urls')),

)
