# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',

    # URLs
    url(r'^', include('oncourse.schools.api_urls')),
    url(r'^', include('oncourse.subjects.api_urls')),

)
