from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from buildings.models import Building

# Create your models here.
class Manager(models.Model):
    user = models.ForeignKey(User, unique=True)
    building = models.ForeignKey(Building, unique=True, blank=True, null=True)
    def __unicode__(self):
        if self.building:
            return "%s - %s"%(self.user, self.building)
        else:
            return "%s - without building"%(self.user)

class SuperAdmin(models.Model):
    user = models.ForeignKey(User, unique=True)
    def __unicode__(self):
        return self.user.username
