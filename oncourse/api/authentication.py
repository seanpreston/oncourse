import logging

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from .models import OAuthConsumer, AccessToken
from datetime import datetime
from annoying.functions import get_object_or_None
from base64 import b64decode


def _strip_header_content(auth_type, header):
    header_split = header.split(' ')
    if header.startswith(auth_type) and len(header_split) > 1:
        content = header_split[1]
        return content
    else:
        return None


class BearerAuthentication():

    def is_authenticated(self, request, **kwargs):
        request.user = AnonymousUser()
        token = _strip_header_content('Bearer', request.META.get('HTTP_AUTHORIZATION', ''))

        if token is not None:
            try:
                token = AccessToken.objects.select_related('user', 'consumer').get(token=token)

            except AccessToken.DoesNotExist:
                logging.error('No token found.')

            else:
                if token.user.is_active and token.consumer.active and (token.expires is None or token.expires > datetime.now()):
                    request.user = token.user
                else:
                    logging.error('Invalid or expired token.')

        return request.user.is_authenticated()


class ConsumerAuthentication():

    def is_authenticated(self, request, **kwargs):
        header_content = _strip_header_content('Basic', request.META.get('HTTP_AUTHORIZATION', ''))
        if header_content is not None:
            decoded_content = b64decode(header_content).split(':')
            if len(decoded_content) > 1:
                client_key = decoded_content[0]
                client_secret = decoded_content[1]
                consumer = get_object_or_None(OAuthConsumer, key=client_key, secret=client_secret)
                if consumer is not None:
                    return True
                else:
                    logging.error('Invalid authentication details.')
            else:
                logging.error('Invalid authentication details.')
        return False
