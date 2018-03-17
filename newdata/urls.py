# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView
from tastypie.api import Api
from .newdata_api import MothRecordResource, MothWaypointResource, MothLocationResource
from . import views

js_info_dict = {
    'packages': ('newdata',),
}

nd_api = Api(api_name='nd')
nd_api.register(MothRecordResource())
nd_api.register(MothWaypointResource())
nd_api.register(MothLocationResource())

urlpatterns = patterns(
    'newdata.views',
    #url(r'^$', TemplateView.as_view(template_name='newdata/newdata_list.html'), name='newdata_browse'),
    url(r'^$', 'datatypes', name='newdata_browse'),
    url(r'^moth/$', views.moth_detail, name='mothdetail'),
    url(r'moth.data/', views.moth_geojson, name='mothgeojson'),
    url(r'moth/(?P<location>.+)/$', views.moth_geojson_filtered, name='mothgeojson_filtered'),
    #url(r'moth/(?P<location>.+)/$', views.moth_geojson_filtered, name='mothgeojson_filtered'),
    url(r'^(?P<pk>[0-9]+)/$', views.DataTypeDetail.as_view(), name='datatypesdetail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DataTypeDetail.as_view(), name='datatypesdetail'),
    url(r'^locations/$', views.mothlocations_list),
    url(r'^locations/(?P<pk>[0-9]+)/$', views.location_detail),
    url(r'^mothupload/$', views.FileUploadViewSet.as_view(), name='mothfileupload'),
    url(r'^mothdownload/(?P<pk>[0-9]+)/$', views.moth_file_download)
)