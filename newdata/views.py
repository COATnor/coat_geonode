# -*- coding: utf-8 -*-
######################################################################
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
########################################################################
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MothLocations, MothFileUpload, MothUploadEvents, MothWaipoints, MothRecords, DataTypes
from .serializers import MothLocationSerializer, MothFileUploadSerializer
import csv
import datetime
import json


@csrf_exempt
def mothlocations_list(request):
    """
    List all moth locations, or create a new location
    :param request:
    :return:
    """

    if request.method == 'GET':
        locations = MothLocations.objects.all()
        serializer = MothLocationSerializer(locations, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MothLocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def location_detail(request, pk):
    """
    Retrieve, update or delete a location
    :param request: 
    :param pk: 
    :return: 
    """

    try:
        location = MothLocations.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MothLocationSerializer(location)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MothLocationSerializer(location, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        location.delete()
        return HttpResponse(status=204)

class FileUploadViewSet(APIView):

    queryset = MothFileUpload.objects.all()
    serializer_class = MothFileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        uploaded_moth_files = MothFileUpload.objects.all()
        serializer = MothFileUploadSerializer(uploaded_moth_files, many=True)
        return Response(serializer.data)


    @csrf_exempt
    def post(self, request, *args, **kwargs):

        # read the uploaded moth data file and save data to db
        self.save_moth_data()

        file_serializer = MothFileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(user=self.request.user, datafile=self.request.data.get('datafile'))
            return Response(file_serializer.data)

    def save_moth_data(self):
        """
        saving data to db. data being read from moth density_trans_year.txt files
        :return:
        """
        datafile = self.request.data.get('datafile')

        content = csv.reader(datafile)
        #content = [x.strip() for x in content]
        for n, i in enumerate(content):
            if n != 0:

                values = i[0].split('\t')
                for e, value in enumerate(values):
                    values[e] = values[e].decode('iso-8859-10')
                try:
                    waypoint = MothWaipoints.objects.get(waypoint_name=values[4])
                    up_event = MothUploadEvents.objects.get(id=1)
                    dateform = datetime.datetime.strptime(values[1], "%d.%m.%Y")
                    new_moth_record = MothRecords.objects.create(date=dateform, alt=values[2], location=values[3], waypoint=waypoint,
                                waypoint_name=values[4], station=values[5], ep=values[6], opl=values[7],
                                opint=values[8], opdark=values[9], opsum=values[10], agr=values[11],
                                obs=values[12], branches=values[13], notes=values[14], upload_event=up_event)
                    new_moth_record.save()
                except:
                    import pdb;
                    pdb.set_trace()
                    print "done"
                    #print new_moth_record

@csrf_exempt
def moth_file_download(request, pk):
    """
    Retrieve, update or delete a location
    :param request:
    :param pk:
    :return:
    """

    try:
        moth_file = MothFileUpload.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MothFileUploadSerializer(moth_file)
        namepath = serializer.data['datafile']
        textfile = moth_file.datafile
        #txt_file = open(path, 'rb')
        filename = namepath.split('/')[-1]
        response = HttpResponse(textfile)
        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response

def datatypes(request):
    """
    This view shows the list of all newdata data types
    """
    datatypes = DataTypes.objects.all()
    return render_to_response("newdata/newdata_list.html",
                              RequestContext(request, {'datatypes': datatypes}))
'''
class DatatypeList(generic.ListView):
    model = DataTypes
    template_name = 'newdata/newdata_list'

    def get_queryset(self):
        return DataTypes.objects.all()
'''
class DataTypeDetail(generic.DetailView):
    model = DataTypes

def moth_detail(request):
    """
        This view manages the details of moth data
    """
    mothdata = MothRecords.objects.all()
    mothlocations = MothLocations.objects.all()
    mothwaypoints = MothWaipoints.objects.all()

    return render_to_response("newdata/moth_detail.html",
                               RequestContext(request, {'mothdata': mothdata,
                                                        'mothloc': mothlocations,
                                                        'mothway': mothwaypoints}))

def moth_geojson(request):
    """
           serializing moth data as geojson
    """

    waypoints_as_geojson = serialize('geojson', MothWaipoints.objects.all())
    return HttpResponse(waypoints_as_geojson, content_type='json')

def moth_waypoints_records(request, waypoint):
    """
               serializing moth data filtered on waypoints
    """

    moth_records_filtered = serialize('json', MothRecords.objects.filter(waypoint_name=waypoint))
    return JsonResponse({'records':moth_records_filtered})

def moth_geojson_filtered(request, location):
    """
        filtering moth data as geojson based on location button pressed
    """
    if request.POST:
        waypoint = request.POST['waypoint']
        moth_records_filtered = serialize('json', MothRecords.objects.filter(waypoint_name=waypoint))
        return HttpResponse(json.dumps({'records': moth_records_filtered}))
    else:
        filtered_waypoints_geojson = serialize('geojson', MothWaipoints.objects.filter(location_name=location))
        filtered_records = serialize('json', MothRecords.objects.filter(location=location))
        return HttpResponse(json.dumps({'way':filtered_waypoints_geojson, 'rec':filtered_records}))