# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url, include
#from django.conf import settings
from django.views.generic import TemplateView
#from tastypie.api import Api
#from .newdata_api import MothRecordResource, MothWaypointResource, MothLocationResource
from . import views

js_info_dict = {
    'packages': ('newdata',),
}

#nd_api = Api(api_name='nd')
#nd_api.register(MothRecordResource())
#nd_api.register(MothWaypointResource())
#nd_api.register(MothLocationResource())

urlpatterns = patterns(
    'newdata.views',
    url(r'^$', TemplateView.as_view(template_name='newdata/newdata_list.html'), name='newdata_browse'),
    url(r'^locations/$', views.mothlocations_list),
    url(r'^locations/(?P<pk>[0-9]+)/$', views.location_detail),
)