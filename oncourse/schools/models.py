from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from oncourse.utils import slugify


class School(models.Model):

    # objects = SubjectManager()

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.CharField(unique=True, max_length=150, db_index=True)

    website = models.URLField(blank=True, null=True)
    twitter = models.CharField(max_length=30, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    email = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(School, self).save(*args, **kwargs)


class Location(models.Model):

    # objects = LocationManager()

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.CharField(unique=True, max_length=150, db_index=True)
    school = models.ForeignKey(School, related_name='locations')

    address = models.CharField(max_length=200, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    email = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)
