# -*- coding: utf-8 -*-
from oncourse.api.views import ApiView, ApiBearerAuthentication
from oncourse.api.decorators import authenticate
from .models import School

import json


class SchoolsListView(ApiView):

    # authentication = [ApiBearerAuthentication()]

    # @authenticate
    def get(self, request, *args, **kwargs):
        offset = int(request.GET.get('offset', '0'), 10)
        limit = int(request.GET.get('limit', '20'), 10)
        if limit > 20:
            limit = 20

        schools = School.objects.all()[offset:limit]
        schools_data = [json.dumps(school.__dict__) for school in schools]

        data = {'objects': schools_data}
        return self.json(data, date_fields=['last_modified', 'created_at',])


class SchoolsView(ApiView):

    # authentication = [ApiBearerAuthentication()]

    # @authenticate
    def get(self, request, school_slug, *args, **kwargs):
        try:
            school = School.objects.get(slug=school_slug)
        except School.DoesNotExist:
            return self.not_found()

        data = school.values()
        return self.json(data, date_fields=['last_modified', 'created_at',])
