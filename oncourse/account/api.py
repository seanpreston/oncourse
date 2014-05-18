# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse, resolve

from oncourse.api.views import ApiView, ApiConsumerAuthentication, ApiBearerAuthentication, ApiMobileAuthentication
from oncourse.api.decorators import authenticate
from oncourse.api.models import AccessToken

import logging
logger = logging.getLogger(__name__)


class LoginView(ApiView):

    authentication = [ApiConsumerAuthentication(), ApiMobileAuthentication()]

    def basic_auth(self, username_or_email, password):
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except (User.DoesNotExist, MultipleObjectsReturned):
                return None

        if user.check_password(password):
            return user
        return None

    def twitter_auth(self, twitter_access_token, twitter_access_secret):
        try:
            user_profile = UserProfile.objects.get(twitter_access_token=twitter_access_token, twitter_access_secret=twitter_access_secret)
        except UserProfile.DoesNotExist:
            return None
        else:
            return user_profile.user
        return None

    def facebook_auth(self, facebook_id, facebook_access_token):
        try:
            user_profile = UserProfile.objects.exclude(facebook_access_token__isnull=True).get(facebook_access_token=facebook_access_token)
        except UserProfile.DoesNotExist:
            try:
                user_profile = UserProfile.objects.get(facebook_id=facebook_id)
            except UserProfile.DoesNotExist:
                return None
            else:
                user_profile.facebook_access_token = facebook_access_token
                user_profile.save()
                return user_profile.user
        else:
            return user_profile.user
        return None


    @authenticate
    def post(self, request, *args, **kwargs):

        try:
            data = self.deserialise(request)
        except ValueError:
            return self.bad_request()

        auth_map = {
            'basic': ('username', 'password'),
            # 'facebook': ('facebook_id', 'facebook_access_token'),
            # 'twitter': ('twitter_access_token', 'twitter_access_secret'),
        }
        user = None

        for auth_type, keys in auth_map.items():
            key, secret = keys
            if data.get(key, '') != '' and data.get(secret, '') != '':
                auth_method = getattr(self, '%s_auth' % auth_type)
                user = auth_method(data[key], data[secret])
                break

        if user is not None and isinstance(user, User) and user.is_authenticated() and user.is_active:
            try:
                access_token = user.access_tokens.get(
                    consumer__key=settings.MASTER_OAUTH_KEY,
                    consumer__secret=settings.MASTER_OAUTH_SECRET
                )
            except AccessToken.DoesNotExist:
                return self.unauthorized()
            else:
                token = access_token.token

            return self.json({'token': token})

        return self.unauthorized()


def load_user(request, user):

    user_data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    # try:
    #     student_profile = user.student_profile
    # except ArtistProfile.DoesNotExist:
    #     user_data['is_student'] = False
    #     user_data['is_verified'] = True
    # else:
    #     user_data['is_student'] = True

    return user_data


class AuthedView(ApiView):

    authentication = [ApiBearerAuthentication()]

    @authenticate
    def get(self, request, *args, **kwargs):
        data = {'user': load_user(request, request.user)}

        return self.json(data)
