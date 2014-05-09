# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from oncourse.utils import slugify


BILLING_TYPES = (
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('semester', 'Semester'),
    ('per-course', 'Per course'),
)


class Subject(models.Model):

    # objects = SubjectManager()

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.CharField(unique=True, max_length=150, db_index=True)
    billing_type = models.CharField(choices=BILLING_TYPES, max_length=20, blank=False, null=False)
    # prerequisites = models.ManyToManyField(Certificate, blank=True, null=True, related_name='')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)
