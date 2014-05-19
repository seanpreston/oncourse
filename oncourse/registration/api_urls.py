# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .api import UserRegistrationView

urlpatterns = patterns(
    '',

    url(r'api/v0/registration/user/$', UserRegistrationView.as_view(), name='api-v0-registration-user'),

)
