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
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MothLocations, MothFileUpload
from .serializers import MothLocationSerializer, MothFileUploadSerializer

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
        file_serializer = MothFileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(user=self.request.user, datafile=self.request.data.get('datafile'))
            return Response(file_serializer.data, status=status.HTTP_200_CREATED)

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