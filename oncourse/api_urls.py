# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',

    # URLs

    # Schools
    url(r'^', include('oncourse.schools.api_urls')),

    # Subjects
    # url(r'^', include('oncourse.subjects.api_urls')),

)
