from django import template

register = template.Library()


def twitter_share_url(user_link, message):
    twitter_url = 'https://twitter.com/share/'
    message = 'text=%s' % message
    rushmore_url = 'url=https://rushmore.fm%s' % user_link
    url = twitter_url + '?' + message + '&' + rushmore_url

    return url
register.simple_tag(twitter_share_url)


def facebook_share_url(user_link):
    facebook_url = 'https://www.facebook.com/sharer/sharer.php'
    rushmore_url = 'u=https://rushmore.fm%s' % user_link
    url = facebook_url + '?' + rushmore_url

    return url
register.simple_tag(facebook_share_url)
