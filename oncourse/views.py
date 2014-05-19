# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from oncourse.auth.views import _login_request, LoginFailure
from oncourse.util.auth import is_authenticated
from oncourse.util.decorators import auth_required

import statsd


def login(request):
    """
    Login page, for which all anonymous users attempting to visit a page without authorization will be redirected to
    """

    if is_authenticated(request):
        return redirect('dash')

    if request.method == 'POST':

        statsd.increment('login.attempt')

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        remember = True if request.POST.get('remember', False) else False

        next = request.POST.get('next', None)

        try:
            token, user_data = _login_request(
                request,
                username=username,
                password=password,
                remember=remember,
            )
        except LoginFailure:
            # If data posted but is invalid for any reason
            statsd.increment('login.failure')
            messages.error(request, "Sorry, those login details aren't valid")
            next = 'login'
        else:
            try:
                resolve(next)
            except:
                next = 'dash'
        return redirect(next)

    else:
        next = request.GET.get('next', 'login')

    login_form = AuthenticationForm()

    return render_to_response(
        'login.html',
        {
            'next': next,
            'login_form': login_form,
            # 'messages': messages,
        },
        context_instance=RequestContext(request)
    )


@auth_required
def dash(request):
    return render_to_response(
        'dash.html',
        {},
        context_instance=RequestContext(request)
    )


def landing(request):
    return render_to_response(
        'landing.html',
        {},
        context_instance=RequestContext(request),
    )
