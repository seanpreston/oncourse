# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

import random


def generate_token():
    return '%032x' % random.getrandbits(128)


class OAuthConsumer(models.Model):

    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, default=generate_token, unique=True, db_index=True)
    secret = models.CharField(max_length=255, default=generate_token, unique=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "api_oauth_consumer"

    def __unicode__(self):
        return u'%s' % self.name


class AccessTokenManager(models.Manager):

    use_for_related_fields = True

    def oncourse(self):
        return self.get_query_set().select_related('consumer').filter(
            consumer__key=settings.MASTER_OAUTH_KEY,
            consumer__secret=settings.MASTER_OAUTH_SECRET
        )

    def get_oncourse(self):
        return self.get_query_set().select_related('consumer').filter(
            consumer__key=settings.MASTER_OAUTH_KEY,
            consumer__secret=settings.MASTER_OAUTH_SECRET
        )


class AccessToken(models.Model):

    token = models.CharField(max_length=32, default=generate_token, unique=True, db_index=True)
    expires = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='access_tokens')
    consumer = models.ForeignKey(OAuthConsumer)

    objects = AccessTokenManager()

    def cache_key(self):
        return 'access-token-%s' % self.token

    def __unicode__(self):
        return u'%s' % self.token


class LastVisited(models.Model):
    user_id = models.IntegerField(primary_key=True)
    activity = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        db_table = "api_last_visited"

    def __unicode__(self):
        return u'%s at %s' % (self.user_id, self.activity)


# Signals
def create_access_token(sender, instance, signal, *args, **kwargs):
    created = kwargs.get('created', False)
    if created:
        consumer = OAuthConsumer.objects.get(key=settings.MASTER_OAUTH_KEY, secret=settings.MASTER_OAUTH_SECRET)
        AccessToken.objects.create(user=instance, consumer=consumer)

models.signals.post_save.connect(create_access_token, sender=User, dispatch_uid="create_user_profile")
