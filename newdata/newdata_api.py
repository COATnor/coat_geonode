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

from .models import MothRecords, MothWaipoints, MothUploadEvents, MothLocations
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authentication import MultiAuthentication, SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from geonode.api.authorization import GeoNodeAuthorization, GeonodeApiKeyAuthentication
from tastypie.resources import ModelResource

class MothLocationResource(ModelResource):
    class Meta:
        queryset = MothLocations.objects.all()
        resource_name = 'mothlocation'
        authentication = GeoNodeAuthorization()
        allowed_methods = ['get', 'post']

class MothWaypointResource(ModelResource):
    class Meta:
        queryset = MothWaipoints.objects.all()
        resource_name = 'mothwaypoint'
        authentication = ApiKeyAuthentication()
        allowed_methods = ['get', 'post']

class MothRecordResource(ModelResource):
    class Meta:
        queryset = MothRecords.objects.all()
        resource_name = 'moth'
        #authentication = ApiKeyAuthentication()
        #authentication = GeoNodeAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(), GeonodeApiKeyAuthentication())
        authorization = DjangoAuthorization()
        allowed_methods = ['get', 'post']

