# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotAllowed, Http404

from oncourse.request import api_call_raw
from oncourse.util.decorators import auth_required

from urlparse import urlparse

import re
import json
import uuid

API_BASE_URL = '/api/'
ALLOWED = ['get', 'post', 'put', 'patch', 'delete']


def proxy(request, api, path):
    print "PROXY"
    if api == '0' or api == '1':
        return _proxy(request, 'v%s' % api, path)
    elif api == 'public':
        return _public_proxy(request, 'v0', path)
    elif api == 'public-1':
        return _public_proxy(request, 'v1', path)
    else:
        raise Http404


def _coalesce(d):
    prog = re.compile(r"(.*)\[([a-zA-Z]+)\]$")
    output = {}
    for key, value in d.items():
        match = prog.match(key)
        if match:
            a, b = match.groups()
            if a not in output:
                output[a] = {}
            output[a][b] = value
        else:
            output[key] = value
    return output


def _munge_post_dict(post_dict):
    munged = {}
    for key, value in dict(post_dict).items():
        if key.endswith('[]'):
            key = key[:-2]
            munged[key] = value
        else:
            munged[key] = value[0]
    return _coalesce(munged)


@auth_required
def _proxy(request, api, path):
    post_dict = {}
    headers = {}
    token = request.session['token']

    method = request.method.lower()
    if 'CONTENT_TYPE' in request.META:
        if request.META['CONTENT_TYPE'].startswith('application/x-www-form-urlencoded'):
            post_dict = request.POST.copy()
            post_dict = _munge_post_dict(post_dict)
        elif request.META['CONTENT_TYPE'].startswith('application/json'):
            post_dict = json.loads(request.body)
        elif request.META['CONTENT_TYPE'].startswith('multipart/form-data'):
            post_dict = request.POST.copy()
            post_dict = _munge_post_dict(post_dict)
            # Don't support file upload for now
            # for key, value in dict(request.FILES.copy()).items():
            #     name = uuid.uuid4().hex
            #     url = s3_upload(name, value[0].read(), allowed_content_types=['image/gif', 'image/png', 'image/jpeg'])
            #     post_dict[key] = url

    if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META:
        method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE'].lower()
    if 'HTTP_X_CSRFTOKEN' in request.META:
        headers['X-CSRFToken'] = request.META['HTTP_X_CSRFTOKEN']
    if '_method' in post_dict:
        method = post_dict['_method'].lower()
        del post_dict['_method']

    refresh = False
    if '_refresh' in post_dict:
        refresh = True
        del post_dict['_refresh']

    if method not in ALLOWED:
        return HttpResponseNotAllowed(ALLOWED)

    full_url = '%s%s/%s' % (API_BASE_URL, api, path)

    if method == 'get' or method == 'delete':
        get_vars = request.GET.copy()
        get_vars.update(post_dict)
        resp = api_call_raw(method, full_url, token=token, headers=headers, get_vars=get_vars)
    else:
        resp = api_call_raw(method, full_url, token=token, headers=headers, get_vars=dict(request.GET), data=post_dict)

    if refresh and (resp.status_code >= 200 and resp.status_code < 300):
        if 'Location' in resp.headers:
            resp = api_call_raw('get', resp.headers['Location'], token=token, get_vars=dict(request.GET))
        else:
            resp = api_call_raw('get', full_url, token=token, get_vars=dict(request.GET))

    content = resp.content
    if content is None or content == '':
        content = ' '
    status_code = resp.status_code
    if status_code == 204:
        status_code = 202

    response = HttpResponse(content, resp.headers['Content-Type'], status_code)
    if 'Location' in resp.headers:
        url = urlparse(resp.headers['Location'])
        response['Location'] = url.path
    if 'X-Date-Fields' in resp.headers:
        response['X-Date-Fields'] = resp.headers['X-Date-Fields']

    return response


def _public_proxy(request, api, path):
    if request.method.lower() != 'get':
        return HttpResponseNotAllowed('get')

    resp = api_call_raw('get', '%s%s/%s' % (API_BASE_URL, api, path), get_vars=dict(request.GET), public=True)
    response = HttpResponse(resp.content, resp.headers['Content-Type'], resp.status_code)

    if 'X-Date-Fields' in resp.headers:
        response['X-Date-Fields'] = resp.headers['X-Date-Fields']

    return response
