# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',

    # URLs

    # Account
    url(r'^', include('oncourse.account.api_urls')),

    # Registration
    url(r'^', include('oncourse.registration.api_urls')),

    # Schools
    url(r'^', include('oncourse.schools.api_urls')),

    # Subjects
    # url(r'^', include('oncourse.subjects.api_urls')),

)
