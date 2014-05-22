# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.serializers import json as django_json
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .serializers import MongoJsonEncoderDecoder
import json

from .authentication import BearerAuthentication, ConsumerAuthentication


class ApiView(View):

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def is_authenticated(self, request):
        for auth in self.authentication:
            if auth.is_authenticated(request):
                return True
        return False

    def is_staff(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Exception

    def filter_data(self, data, fields):
        filtered_data = {}

        for field in fields:
            attr_name = self.field_map.get(field, None)
            if attr_name is not None:
                if hasattr(getattr(data, attr_name), '__call__'):
                    filtered_data[field] = getattr(data, attr_name)()
                else:
                    filtered_data[field] = getattr(data, attr_name)

        return filtered_data

    def convert_empty_strings(self, data):
        for key, value in data.items():
            if value == '':
                data[key] = None
        return data

    def validate_fields(self, data, field_map):
        # Fails if: submitted data contains unrecognized fields, doesn't contain all required fields
        # Returns: set of non-required but recognized fields provided
        provided_fields = set(data.keys())
        accepted_fields = set([field.get('name') for field in field_map])
        required_fields = set([field.get('name') for field in field_map if field.get('required', True)])

        #  Ensures provided data doesn't contain unaccepted fields
        if not provided_fields.issubset(accepted_fields):
            # unrecognized_fields = accepted_fields.difference(provided_fields)
            # raise ValidationError('Fields: %s are not recognized.' % ', '.join(map(str(unrecognized_fields))))
            raise ValidationError("Unrecognised fields were provided.")

        #  Ensures all required fields are provided
        if not required_fields.issubset(provided_fields):
            # missing_fields = required_fields.difference(provided_fields)
            # raise ValidationError('Fields: %s are missing or invalid.' % ', '.join(map(str(missing_fields))))
            raise ValidationError("Not all requried fields were provided.")

        #  TODO run through munger
        return data

    def apply_filters(self, objects, request):
        filter_kwargs = {}
        for filter_field in self.filter_fields:
            filter_name = filter_field['name']
            if filter_name in request.GET.keys():
                if filter_field.has_key('munger'):
                    munge_method = getattr(self, filter_field['munger'])
                    filter_kwargs[filter_name] = munge_method(request.GET[filter_name])
                else:
                    filter_kwargs[filter_name] = request.GET[filter_name]
        if filter_kwargs != {}:
            filtered_objects = objects.filter(**filter_kwargs)
        else:
            filtered_objects = objects
        return filtered_objects

    def safe_bool(self, data):
        if isinstance(data, bool):
            return data
        elif data == 'true':
            return True
        elif data == 'false':
            return False
        else:
            raise TypeError

    def safe_url(self, data):
        val = URLValidator(verify_exists=False)
        val(data)

    def safe_int(self, get_dict, key, fallback, maximum=None):
        try:
            value = int(get_dict.get(key, fallback))
            if value < 0:
                value = 0
        except (ValueError, TypeError):
            value = fallback
        if maximum is not None and value > maximum:
            value = maximum
        return value

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ApiView, self).dispatch(*args, **kwargs)

    def serialise(self, data):
        return json.dumps(data, cls=django_json.DjangoJSONEncoder, sort_keys=True, ensure_ascii=False).replace('/', '\\/')

    def deserialise(self, request):
        return json.loads(request.body)

    #  TODO revisit this, lazy!
    @staticmethod
    def mongo_serialise(data):
        data = json.loads(json.dumps(data, cls=MongoJsonEncoderDecoder))
        return data

    #  TODO deprecate this
    def json(self, data, date_fields=None, status=200, headers=None):
        response = HttpResponse(content_type='application/json; charset=UTF-8', status=status)
        if date_fields is not None:
            response['x-date-fields'] = ','.join(date_fields)
        if headers is not None:
            for key, value in headers.items():
                response[key] = value
        if not isinstance(data, str):
            response.content = self.serialise(data)
        else:
            response.content = data
        return response

    def json_response(self, data, date_fields=None, status=200, *args, **kwargs):
        return self.json(data, date_fields, status, *args, **kwargs)

    def created(self, location=None):
        resp = HttpResponse(status=201)
        if location is not None:
            resp['Location'] = location
        return resp

    def accepted(self, content='Accepted'):
        return HttpResponse(content, status=202)

    def no_content(self, content='No content'):
        return HttpResponse(content, status=204)

    def bad_request(self, content='Bad request'):
        return HttpResponse(content, status=400)

    def unauthorized(self, content='Unauthorized'):
        return HttpResponse(content, status=401)

    def forbidden(self, content='Forbidden'):
        return HttpResponse(content, status=403)

    def not_found(self, content='Not found'):
        return HttpResponse(content, status=404)

    def not_allowed(self, content='Not allowed'):
        return HttpResponse(content, status=405)

    def conflict(self, content='Conflict'):
        return HttpResponse(content, status=409)

    def resource_expired(self, content='Resource expired'):
        return HttpResponse(content, status=410)

    def has_extension(self, request, extension):
        extensions = request.GET.getlist('_extensions', [])
        return extension in extensions

    def load_object(self, obj):
        fields = obj._meta.get_all_field_names()
        manager_fields = [field.get_accessor_name() for field in obj._meta.get_all_related_objects()]
        fields = set(fields) - set(manager_fields)

        data = {}
        for field in fields:
            data[field] = getattr(obj, field)

        return data


class ApiPublicAuthentication(object):

    #  TODO check separately and return 405
    http_method_names_override = ['get']

    def is_authenticated(self, request):
        if request.method.lower() in self.http_method_names_override:
            return True
        return False


class ApiBearerAuthentication(object):

    def is_authenticated(self, request):
        auth = BearerAuthentication()
        # Modifies request.user
        return auth.is_authenticated(request)


class ApiMobileAuthentication(object):

    def is_authenticated(self, request):
        return True


class ApiConsumerAuthentication(object):

    def is_authenticated(self, request):
        auth = ConsumerAuthentication()
        # Modifies request.user
        return auth.is_authenticated(request)
