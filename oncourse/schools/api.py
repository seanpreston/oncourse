# -*- coding: utf-8 -*-
from oncourse.api.views import ApiView, ApiBearerAuthentication
from api.decorators import authenticate
from .models import School

import json


class SchoolsView(ApiView):

    authentication = [ApiBearerAuthentication()]

    @authenticate
    def get(self, request, *args, **kwargs):
        offset = int(request.GET.get('offset', '0'), 10)
        limit = int(request.GET.get('limit', '20'), 10)
        if limit > 20:
            limit = 20

        schools = School.objects.all()[offset:limit]
        schools_data = [json.dumps(school.__dict__) for school in schools]

        data = {'objects': schools_data}
        return self.json(data)
