from django.contrib import messages
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from oncourse.auth.views import RegistrationFailure, AuthFailure
from oncourse.request import api_call
from oncourse.util.auth import is_authenticated

import statsd


def index(request):

    return redirect('registration-user')

    return render_to_response(
        'registration/index.html',
        {},
        context_instance=RequestContext(request)
    )


def _create_user(request, **kwargs):
    res, status = api_call('post', '/api/v0/registration/user/', data=kwargs)

    if status != 200 or 'token' not in res:
        raise RegistrationFailure

    token = res['token']
    data, status = api_call('get', '/api/v0/account/authed/', token=token)

    if status != 200 or data is None:
        raise AuthFailure()

    statsd.increment('registration.success')
    for key, val in data.items():
        request.session[key] = val
    request.session['token'] = token

    return token, data


def register_user(request):

    if is_authenticated(request):
        return redirect('dash')

    if request.method == 'POST':

        statsd.increment('registration.attempt')

        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password_confirm = request.POST.get('password_confirm', None)

        if password != password_confirm:
            messages.error(request, "Your passwords did not match")
            return redirect('registration-user')

        next = request.POST.get('next', None)

        try:
            token, user_data = _create_user(
                request,
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
        except RegistrationFailure:
            # If data posted but is invalid for any reason
            statsd.increment('registration.failure')
            messages.error(request, "Sorry, those registration details aren't valid")
            next = 'registration-user'
        else:
            try:
                resolve(next)
            except:
                next = 'dash'
        return redirect(next)

    return render_to_response(
        'registration/user.html',
        {},
        context_instance=RequestContext(request),
    )
