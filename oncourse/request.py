# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import QueryDict
from django.utils.encoding import iri_to_uri

from base64 import b64encode
from datetime import datetime, date
# from metrics import Timer

import erequests
import json
import logging
import requests
import statsd

logger = logging.getLogger(__name__)


def _encode(get_var_val):
    if isinstance(get_var_val, datetime):
        return get_var_val.isoformat()
    elif isinstance(get_var_val, date):
        return get_var_val.isoformat()
    else:
        return get_var_val


def _listify_values(input_vars):
    output_vars = {}
    for key, val in input_vars.items():
        if not isinstance(val, list):
            output_vars[key] = [val]
        else:
            output_vars[key] = val
    return output_vars


def _encode_get_vars(get_vars):
    encoded_get_vars = {}

    if isinstance(get_vars, QueryDict):
        get_vars = dict(get_vars)
    else:
        get_vars = _listify_values(get_vars)

    for key, vals in get_vars.items():
        encoded_val = [_encode(nested_val) for nested_val in vals]
        encoded_get_vars[key] = encoded_val
    return encoded_get_vars


# Make this more resilient to (not) having correctly formed uris
def build_url(uri, get_vars=None):

    if get_vars is not None:
        encoded_get_vars = _encode_get_vars(get_vars)
    else:
        encoded_get_vars = {}

    api_url = '%s%s' % (settings.API_BASE, uri)

    try:
        key, val = encoded_get_vars.popitem()  # Pop item, to correctly format the URL
    except KeyError:
        pass
    else:
        if isinstance(val, list):
            api_url = '%s?%s=%s' % (api_url, key, val.pop(0))  # Pop first to maintain order of vars, can be sensitive for ordering, etc.
            for further_get_var in val:
                api_url = '%s&%s=%s' % (api_url, key, further_get_var)
        else:
            api_url = '%s?%s=%s' % (api_url, key, val)

    for key, val in encoded_get_vars.items():
        if isinstance(val, list):
            for further_get_var in val:
                api_url = '%s&%s=%s' % (api_url, key, further_get_var)
        else:
            api_url = '%s&%s=%s' % (api_url, key, val)

    return iri_to_uri(api_url)


def date_handler(obj):

    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


def deserialise(content):
    try:
        res = json.loads(content)
    except ValueError:
        logger.error("Could not decode JSON: %s", content)
        res = None

    return res


def build_auth():
    # Add some stuff for basic auth
    if hasattr(settings, 'API_AUTH'):
        auth = (settings.API_AUTH['user'], settings.API_AUTH['password'])
    else:
        auth = None

    #prefix = len("%s/api/v0" % settings.API_BASE)
    name = "api_request"

    def pre_request(request):
        #print "REQ %i START" % id(request)
        # Timer.start((name, id(request)))
        return None

    def post_request(request):
        # obj_id = (name, id(request))
        # elapsed = Timer.elapsed(obj_id)
        #print "REQ %i END in %i" % (id(request), elapsed * 1000)
        # Timer.accumulate(elapsed)
        return None

 #   hooks = {
        # 'pre_request': pre_request,
        # 'post_request': post_request,
#    }

    return auth


def api_async(params, token=None):
    """
    Takes the uris of the API to call
    """
    headers = {}
    keys = []
    urls = []

    for key, value in params.items():
        method, uri, get_vars = value
        keys.append(key)
        urls.append((method, build_url(uri, get_vars)))

    if token is not None:
        headers['Authorization'] = 'Bearer %s' % token
    else:
        encoded_consumer = b64encode('%s:%s' % (settings.MASTER_OAUTH_KEY, settings.MASTER_OAUTH_SECRET))
        headers['Authorization'] = 'Basic %s' % encoded_consumer

    reqs = (erequests.get(url, headers=headers) for method, url in urls)
    reqs_map = erequests.map(reqs)
    return dict(zip(keys, reqs_map))


def api_call_raw(method, uri, token=None, headers=None, get_vars=None, data=None, public=False):
    """
    Takes the uri of an application URL to call
    """
    statsd.increment('api.call')

    if not headers:
        headers = {}

    if data is not None:
        data = json.dumps(data, default=date_handler)
        headers['Content-Type'] = 'application/json'

    if not public:
        if token is not None:
            headers['Authorization'] = 'Bearer %s' % token
        else:
            encoded_consumer = b64encode('%s:%s' % (settings.MASTER_OAUTH_KEY, settings.MASTER_OAUTH_SECRET))
            headers['Authorization'] = 'Basic %s' % encoded_consumer

    api_url = build_url(uri, get_vars)

    auth = build_auth()
    req = requests.request(method, api_url, headers=headers, data=data, auth=auth, timeout=90)
    return req


def _parse_date(obj, field):
    if '__' in field:
        key, item_field = field.split('__', 1)
        obj[key] = [_parse_date(o, item_field) for o in obj[key]]
    else:
        obj[field] = _decode_datetime(obj[field])
    return obj


def _decode_datetime(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except (TypeError, ValueError):
        try:
            return datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f")
        except (TypeError, ValueError):
            try:
                return datetime.strptime(d, "%Y-%m-%dT%H:%M:%S")
            except (TypeError, ValueError):
                try:
                    return datetime.strptime(d, "%H:%M:%S")
                except (TypeError, ValueError):
                    pass
            pass
    return None


def _fix_dates(d, date_fields):
    for field in date_fields:
        if '__' in field and 'objects' not in d:
            key, item_field = field.split('__', 1)
        else:
            key, item_field = 'objects', field
        if key in d:
            d[key] = [_parse_date(obj, item_field) for obj in d[key]]
        else:
            _parse_date(d, field)
    return d


def _deserialise_response(response):
    if response.headers['content-type'].startswith('application/json'):
        data = deserialise(response.content)
        date_fields = []
        if 'X-Date-Fields' in response.headers:
            date_fields = response.headers['X-Date-Fields'].split(',')
        return _fix_dates(data, date_fields)
    else:
        logger.error("Backend returned non-JSON response: %s", response.content)
        return None


def api_call(method, uri, token=None, get_vars=None, data=None, public=False):
    """
    Takes the uri of an application URL to call
    """
    response = api_call_raw(method, uri, token=token, get_vars=get_vars, data=data, public=public)
    return _deserialise_response(response), response.status_code


def api_list(uri, token=None, get_vars=None):
    data, status = api_call('get', uri, token=token, get_vars=get_vars)
    return data
