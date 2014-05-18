from oncourse.util import cache
from oncourse.request import api_call

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect


def _is_authed(request):
    session_keys = request.session.keys()

    if 'token' in session_keys and 'user' in session_keys:
        return True
    return False


def auth_required(fn):
    def wrapped(request, *args, **kwargs):
        if _is_authed(request):
            token = request.session['token']
            username = request.session['user']['username']
            ckey = 'access-token-%s' % token
            token_username = cache.get(ckey, None)

            # Cached token has expired, been removed (and subsequently from cache) or assigned to a different user
            if token is None or token_username != username:
                data, status = api_call('get', '/api/v0/account/authed/', token=token)
                if status == 200 and data['user']['username'] == username:
                    request.session['user'] = data['user']
                    cache.set(ckey, username, settings.CACHE_TIMEOUT)
                else:
                    request.session.flush()
                    return redirect('login')

            return fn(request, *args, **kwargs)
        request.session.flush()
        return redirect('login')
    return wrapped