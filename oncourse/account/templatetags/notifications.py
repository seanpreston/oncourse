from django import template
from rushmore.request import api_call
import time
from django.core.urlresolvers import reverse
from django.utils.translation import ungettext, ugettext
import datetime

register = template.Library()


def render_notifications(token, user):
    data, status = api_call('get', '/api/v1/notifications/', token=token)
    notifications = data['notifications']
    unviewed_count = sum(not n['viewed'] for n in notifications)
    clear_notifications_uri = reverse('api-v1-notifications')
    now = int(time.time())

    return {
        'notifications': notifications,
        'unviewed_count': unviewed_count,
        'clear_notifications_uri': clear_notifications_uri,
        'now': now,
        'username': user['username'],
    }
register.inclusion_tag('account/notifications.html')(render_notifications)


@register.filter
def time_since(timestamp):
    if not timestamp:
        return ""

    delta = datetime.datetime.now() - timestamp
    count = 0

    if delta.days == 0:
        chunks = (
            (3600.0, lambda n: ungettext('hour', 'hours', n)),
            (60, lambda n: ungettext('minute', 'minutes', n)),
            (1.0, lambda n: ungettext('second', 'seconds', n)),
        )
        attr = 'seconds'
    elif delta.days == -1:
        return u"yesterday"
    else:
        chunks = (
            (365.0, lambda n: ungettext('year', 'years', n)),
            (30.0, lambda n: ungettext('month', 'months', n)),
            (7.0, lambda n: ungettext('week', 'weeks', n)),
            (1.0, lambda n: ungettext('day', 'days', n)),
        )
        attr = 'days'

    for i, (chunk, name) in enumerate(chunks):
        if abs(getattr(delta, attr)) >= chunk:
            count = abs(round(getattr(delta, attr) / chunk, 0))
            break

    date_str = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}

    return date_str + " ago"
