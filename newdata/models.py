# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 NINA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################


# from django.db import models
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class DataTypes(models.Model):
    type_name = models.CharField(max_length=10)


class MothLocations(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class MothWaipoints(models.Model):
    waypoint_name = models.CharField(max_length=10)
    location = models.ForeignKey(MothLocations)
    location_name = models.CharField(max_length=15)
    station = models.PositiveSmallIntegerField()
    utm33_lon = models.FloatField()
    utm33_lat = models.FloatField()
    lon = models.FloatField()
    lat = models.FloatField()
    mpoint = models.PointField(srid=4326)

class MothUploadEvents(models.Model):
    upload_date = models.DateTimeField()
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL)

class MothRecords(models.Model):
    date = models.DateTimeField()
    alt = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=12)
    waypoint = models.ForeignKey(MothWaipoints)
    waypoint_name = models.CharField(max_length=12)
    station = models.PositiveSmallIntegerField()
    ep = models.PositiveIntegerField()
    opl = models.PositiveIntegerField()
    opint = models.PositiveIntegerField()
    opdark = models.PositiveIntegerField()
    opsum = models.PositiveIntegerField()
    agr = models.PositiveIntegerField()
    obs = models.CharField(max_length=12)
    branches = models.PositiveSmallIntegerField()
    notes = models.CharField(max_length=150)
    upload_event = models.ForeignKey(MothUploadEvents)

# probably the user foreignkey needs to be changed -- look into geonode user management
class MothFileUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id')
    datafile = models.FileField()


