# -*- coding: utf-8 -*-
from django.http import HttpResponse


def authenticate(fn):
    def wrapper(self, request, *args, **kwargs):
        # TODO: Remove after auth is added
        # return fn(self, request, *args, **kwargs)
        if not self.is_authenticated(request):
            return HttpResponse('Unauthorized', status=401)

        return fn(self, request, *args, **kwargs)
    return wrapper
