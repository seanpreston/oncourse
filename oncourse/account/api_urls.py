# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .api import LoginView, AuthedView


urlpatterns = patterns(
    '',

    # Auth
    url(r'api/v0/account/login/$', LoginView.as_view(), name='api-v0-login'),
    url(r'api/v0/account/authed/$', AuthedView.as_view(), name='api-v0-authed'),

)
