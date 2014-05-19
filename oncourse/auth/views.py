# -*- coding: utf-8 -*-
from oncourse.request import api_call

import statsd

import logging
logger = logging.getLogger(__name__)

class RegistrationFailure(Exception):
    pass

class LoginFailure(Exception):
    pass

class AuthFailure(Exception):
    pass

def _login_request(request, remember=True, *args, **kwargs):
    res, status = api_call('post', '/api/v0/account/login/', data=kwargs)

    if status != 200 or 'token' not in res:
        raise LoginFailure()

    token = res['token']
    data, status = api_call('get', '/api/v0/account/authed/', token=token)

    if status != 200 or data is None:
        raise AuthFailure()

    statsd.increment('login.success')
    for key, val in data.items():
        request.session[key] = val
    request.session['token'] = token
    if remember:
        request.session.set_expiry(0)
    return token, data