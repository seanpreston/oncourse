from django import template
from django.conf import settings

import hashlib
from rushmore.request import api_call
from rushmore.util import cache

register = template.Library()

if settings.DEBUG:
    STATS_TIMEOUT = 10
else:
    STATS_TIMEOUT = 60 * 60  # An hour


def _get_user_stats(username):
    ckey = hashlib.md5('%s-stats-frontend' % username).hexdigest()
    stats = cache.get(ckey)
    if stats is None:
        stats, status_code = api_call('get', '/api/v1/profile-stats/%s/' % username)
        cache.set(ckey, stats, STATS_TIMEOUT)
    return stats


def render_sparta_sidebar(request_username, profile_user):
    stats = _get_user_stats(profile_user['username'])
    sparta_stats = {
        'current_rank': stats['current_rank'],
        'contrib_count': stats['contrib_count'],
        'profile_user': profile_user,
        'request_username': request_username,
    }
    return sparta_stats
register.inclusion_tag('account/sparta_sidebar.html')(render_sparta_sidebar)


def render_sticker_sidebar(request_username, profile_user):
    stats = _get_user_stats(profile_user['username'])
    user_stickers = stats['user_stickers']
    sticker_stats = {
        'user_stickers': user_stickers,
        'request_username': request_username,
        'profile_user': profile_user,
        'stickers_earned': stats['stickers_earned'],
        'total_stickers': stats['total_stickers'],
    }
    return sticker_stats
register.inclusion_tag('account/sticker_sidebar.html')(render_sticker_sidebar)
